MPY-CROSS ?= ~/Downloads/mpy-cross.static-amd64-linux-8.0.5
DEST ?= /media/CIRCUITPY/

objects = code.mpy secrets.mpy label.mpy powerwallservice.mpy style.mpy timeservice.mpy weatherservice.mpy

all: $(objects) $(DEST)/code.py
.PHONY: all

$(objects): %.mpy: %.py

%.mpy: %.py
	@echo building $@
	$(MPY-CROSS) $<
	cp $@ $(DEST)

$(DEST)/code.py: code.py
	cp $? $(DEST)
