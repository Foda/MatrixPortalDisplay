import time
from random import randrange
import board
import terminalio
import displayio
from adafruit_display_text.label import Label

WEATHER_CLEAR = (['clear', 'fair'], 0)
WEATHER_PART_CLOUDY = (['few clouds', 'broken clouds'], 2)
WEATHER_CLOUDY = (['scattered clouds'], 6)
WEATHER_STORM = (['thunderstorm'], 4)
WEATHER_RAIN = (['rain', 'drizzle', 'showers'], 8)
WEATHER_HAZE = (['overcast', 'dust', 'fog', 'smoke', 'mist', 'haze'], 10)

KNOWN_WEATHER = [
    WEATHER_CLEAR,
    WEATHER_PART_CLOUDY,
    WEATHER_CLOUDY,
    WEATHER_STORM,
    WEATHER_RAIN,
    WEATHER_HAZE,
]

class Weather(displayio.Group):
    def __init__(self, display, icons, tiny_font, med_font):
        super().__init__()
        self.display = display

        self.tiny_font = tiny_font
        self.med_font = med_font

        # Time
        self.time_text = Label(self.med_font)
        self.time_text.x = 1
        self.time_text.y = 23
        self.time_text.color = 0xA8995E
        self.time_text.text = '??:??'
        self.append(self.time_text)

        self.am_pm = Label(self.tiny_font)
        self.am_pm.x = 64
        self.am_pm.y = 23
        self.am_pm.color = 0x7F7F7F
        self.am_pm.text = 'PM'
        self.append(self.am_pm)

        # Temperature
        self.temp_text = Label(self.med_font)
        self.temp_text.x = 1
        self.temp_text.y = 4
        self.temp_text.color = 0x800000
        self.temp_text.text = '??'
        self.append(self.temp_text)

        self.degree_text = Label(self.tiny_font)
        self.degree_text.x = 24
        self.degree_text.y = 4
        self.degree_text.color = 0x7F7F7F
        self.degree_text.text = 'F'
        self.append(self.degree_text)

        self.description_text = Label(self.tiny_font)
        self.description_text.x = 2
        self.description_text.y = self.temp_text.height - 7
        self.description_text.color = 0x7F7F7F
        self.description_text.text = 'Loading'

        # Scroller group for the weather description since it needs to scroll
        self.scroll_group = displayio.Group()
        self.scroll_group.append(self.description_text)
        self.append(self.scroll_group)

        self.icon_sprite = displayio.TileGrid(
            icons,
            pixel_shader=icons.pixel_shader,
            tile_width=10,
            tile_height=10,
            x=53,
            y=1
        )
        self.icon_sprite[0] = 1
        self.append(self.icon_sprite)


    def update_weather(self, the_weather):
        weather_main = the_weather.get('main')

        temp_degrees = int(weather_main.get('temp'))
        self.temp_text.text = str(temp_degrees)

        if temp_degrees < 35: 
            self.temp_text.color = 0x09B3D4 # Blueish
        elif temp_degrees < 50: 
            self.temp_text.color = 0x43E05C # Greenish
        elif temp_degrees < 70:
            self.temp_text.color = 0xACE33B # Greenish
        elif temp_degrees < 80:
            self.temp_text.color = 0xE8E527 # Yellow
        elif temp_degrees < 90:
            self.temp_text.color = 0xFFB325 # orange
        else:
            self.temp_text.color = 0x800000

        # Might need to move degree symbol over if it's 3 digits
        self.degree_text.x = self.temp_text.width + 2

        weather_condition = the_weather.get('weather')[0]
        description = weather_condition.get('description').lower()

        if description == "broken clouds":
            self.description_text.text = "broke-ass clouds"
        else:
            self.description_text.text = description
        
        # Try and match description to an icon
        weather_icon = WEATHER_CLEAR
        for weather_type in KNOWN_WEATHER:
            if any(item in description for item in weather_type[0]):
                weather_icon = weather_type
                break

        # The second column in the weather sprite sheet is the night
        # versions of the icons
        icon_idx = weather_icon[1]
        if time.localtime().tm_hour >= 18 or time.localtime().tm_hour <= 5:
            icon_idx += 1
        self.icon_sprite[0] = icon_idx


    def update_time(self):
        current = time.localtime()
        actual_hour = current.tm_hour

        if actual_hour > 12:
            self.time_text.text = "{:d}:{:02d}".format(actual_hour - 12, current.tm_min)
        else:
            self.time_text.text = "{:d}:{:02d}".format(actual_hour, current.tm_min)

        self.am_pm.x = self.time_text.width + 4
        self.am_pm.text = 'PM' if actual_hour > 12 else 'AM'


    def set_description_hidden(self, is_hidden):
        self.scroll_group.hidden = is_hidden


    def update_scroll(self):
        if self.description_text.width < 64:
            return

        text_width = self.description_text.bounding_box[2]
        for _ in range(text_width + 1):
            self.scroll_group.x = self.scroll_group.x - 1
            time.sleep(0.06)

        # Reset position to off the screen and scroll it back into the start
        # position
        self.scroll_group.x = 32
        for _ in range(32):
            self.scroll_group.x = self.scroll_group.x - 1
            time.sleep(0.06)
