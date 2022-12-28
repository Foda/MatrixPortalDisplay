import time
from random import randrange
import board
import terminalio
import displayio
from adafruit_display_text.label import Label

class NowPlaying(displayio.Group):
    def __init__(self, display, icons, tiny_font, med_font, *):
        super().__init__()
        self.display = display

        self.tiny_font = tiny_font
        self.med_font = med_font
        
        self.description_text = Label(self.tiny_font)
        self.description_text.x = 11
        self.description_text.y = 15
        self.description_text.color = 0x7F7F7F
        self.description_text.text = 'N/A'

        self.scroll_group = displayio.Group()
        self.scroll_group.append(self.description_text)
        self.append(self.scroll_group)
        
        self.spotify_sprite = displayio.TileGrid(
            icons,
            pixel_shader=icons.pixel_shader,
            x=0,
            y=11,
            tile_width=10,
            tile_height=10,
        )
        self.spotify_sprite[0] = 12
        self.append(self.spotify_sprite)
        
        self.hidden = True


    def update_now_playing(self, song, artist):
        self.description_text.text = f'{song} - {artist}' 
    

    def update_scroll(self):
        if self.description_text.width < 52 or self.hidden:
            return

        text_width = self.description_text.bounding_box[2]
        for _ in range(text_width + 1):
            self.scroll_group.x = self.scroll_group.x - 1
            time.sleep(0.06)

        # Reset position to off the screen and scroll it back into the start
        # position
        self.scroll_group.x = 64
        for _ in range(64):
            self.scroll_group.x = self.scroll_group.x - 1
            time.sleep(0.06)
