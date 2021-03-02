
import SH1106
import RPi.GPIO as GPIO
import time

from PIL import Image, ImageDraw, ImageFont

from button_enum import ButtonType

from event import *

#GPIO define
RST_PIN        = 25
CS_PIN         = 8
DC_PIN         = 24

KEY_UP_PIN     = 6
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13

KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

#LCD_WIDTH = 128
#LCD_HEIGHT = 64


class OLEDHat():
    def __init__(self):
        self._disp = SH1106.SH1106()
        self._disp.Init()

        # Clear display.
        self._disp.clear()

        # init GPIO
        # for P4:
        # sudo vi /boot/config.txt
        # gpio=6,19,5,26,13,21,20,16=pu
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up

        self._button_pressing = [False for i in range(ButtonType.BUTTON_COUNT)]

    @property
    def width(self):
        return self._disp.width

    @property
    def height(self):
        return self._disp.height

    def display(self, image):
        self._disp.ShowImage(self._disp.getbuffer(image))

    def update(self, event_queue):
        if GPIO.input(KEY_UP_PIN):  # button is released
            if self._button_pressing[ButtonType.STICK_UP] == True:
                event_queue.put_nowait(ButtonUpEvent(ButtonType.STICK_UP))
            self._button_pressing[ButtonType.STICK_UP] = False
        else:  # button is pressed:
            if self._button_pressing[ButtonType.STICK_UP] == False:
                event_queue.put_nowait(ButtonDownEvent(ButtonType.STICK_UP))
            self._button_pressing[ButtonType.STICK_UP] = True

        if GPIO.input(KEY_LEFT_PIN):  # button is released
            if self._button_pressing[ButtonType.STICK_LEFT] == True:
                event_queue.put_nowait(ButtonUpEvent(ButtonType.STICK_LEFT))
            self._button_pressing[ButtonType.STICK_LEFT] = False
        else:  # button is pressed:
            if self._button_pressing[ButtonType.STICK_LEFT] == False:
                event_queue.put_nowait(ButtonDownEvent(ButtonType.STICK_LEFT))
            self._button_pressing[ButtonType.STICK_LEFT] = True

        if GPIO.input(KEY_RIGHT_PIN):  # button is released
            if self._button_pressing[ButtonType.STICK_RIGHT] == True:
                event_queue.put_nowait(ButtonUpEvent(ButtonType.STICK_RIGHT))
            self._button_pressing[ButtonType.STICK_RIGHT] = False
        else:  # button is pressed:
            if self._button_pressing[ButtonType.STICK_RIGHT] == False:
                event_queue.put_nowait(ButtonDownEvent(ButtonType.STICK_RIGHT))
            self._button_pressing[ButtonType.STICK_RIGHT] = True

        if GPIO.input(KEY_DOWN_PIN):  # button is released
            if self._button_pressing[ButtonType.STICK_DOWN] == True:
                event_queue.put_nowait(ButtonUpEvent(ButtonType.STICK_DOWN))
            self._button_pressing[ButtonType.STICK_DOWN] = False
        else:  # button is pressed:
            if self._button_pressing[ButtonType.STICK_DOWN] == False:
                event_queue.put_nowait(ButtonDownEvent(ButtonType.STICK_DOWN))
            self._button_pressing[ButtonType.STICK_DOWN] = True

        if GPIO.input(KEY_PRESS_PIN):  # button is released
            if self._button_pressing[ButtonType.STICK_PRESS] == True:
                event_queue.put_nowait(ButtonUpEvent(ButtonType.STICK_PRESS))
            self._button_pressing[ButtonType.STICK_PRESS] = False
        else:  # button is pressed:
            if self._button_pressing[ButtonType.STICK_PRESS] == False:
                event_queue.put_nowait(ButtonDownEvent(ButtonType.STICK_PRESS))
            self._button_pressing[ButtonType.STICK_PRESS] = True

        if GPIO.input(KEY1_PIN):  # button is released
            if self._button_pressing[ButtonType.BUTTON_1] == True:
                event_queue.put_nowait(ButtonUpEvent(ButtonType.BUTTON_1))
            self._button_pressing[ButtonType.BUTTON_1] = False
        else:  # button is pressed:
            if self._button_pressing[ButtonType.BUTTON_1] == False:
                event_queue.put_nowait(ButtonDownEvent(ButtonType.BUTTON_1))
            self._button_pressing[ButtonType.BUTTON_1] = True

        if GPIO.input(KEY2_PIN):  # button is released
            if self._button_pressing[ButtonType.BUTTON_2] == True:
                event_queue.put_nowait(ButtonUpEvent(ButtonType.BUTTON_2))
            self._button_pressing[ButtonType.BUTTON_2] = False
        else:  # button is pressed:
            if self._button_pressing[ButtonType.BUTTON_2] == False:
                event_queue.put_nowait(ButtonDownEvent(ButtonType.BUTTON_2))
            self._button_pressing[ButtonType.BUTTON_2] = True

        if GPIO.input(KEY3_PIN):  # button is released
            if self._button_pressing[ButtonType.BUTTON_3] == True:
                event_queue.put_nowait(ButtonUpEvent(ButtonType.BUTTON_3))
            self._button_pressing[ButtonType.BUTTON_3] = False
        else:  # button is pressed:
            if self._button_pressing[ButtonType.BUTTON_3] == False:
                event_queue.put_nowait(ButtonDownEvent(ButtonType.BUTTON_3))
            self._button_pressing[ButtonType.BUTTON_3] = True

    def test_run(self):
        image = Image.new('1', (self._disp.width, self._disp.height), "WHITE")

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # try:
        while 1:
            # with canvas(device) as draw:
            if GPIO.input(KEY_UP_PIN):  # button is released
                draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  # Up
            else:  # button is pressed:
                draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  # Up filled
                print("Up")

            if GPIO.input(KEY_LEFT_PIN):  # button is released
                draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  # left
            else:  # button is pressed:
                draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)  # left filled
                print("left")

            if GPIO.input(KEY_RIGHT_PIN):  # button is released
                draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0)  # right
            else:  # button is pressed:
                draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1)  # right filled
                print("right")

            if GPIO.input(KEY_DOWN_PIN):  # button is released
                draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0)  # down
            else:  # button is pressed:
                draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1)  # down filled
                print("down")

            if GPIO.input(KEY_PRESS_PIN):  # button is released
                draw.rectangle((20, 22, 40, 40), outline=255, fill=0)  # center
            else:  # button is pressed:
                draw.rectangle((20, 22, 40, 40), outline=255, fill=1)  # center filled
                print("center")

            if GPIO.input(KEY1_PIN):  # button is released
                draw.ellipse((70, 0, 90, 20), outline=255, fill=0)  # A button
            else:  # button is pressed:
                draw.ellipse((70, 0, 90, 20), outline=255, fill=1)  # A button filled
                print("KEY1")

            if GPIO.input(KEY2_PIN):  # button is released
                draw.ellipse((100, 20, 120, 40), outline=255, fill=0)  # B button]
            else:  # button is pressed:
                draw.ellipse((100, 20, 120, 40), outline=255, fill=1)  # B button filled
                print("KEY2")

            if GPIO.input(KEY3_PIN):  # button is released
                draw.ellipse((70, 40, 90, 60), outline=255, fill=0)  # A button
            else:  # button is pressed:
                draw.ellipse((70, 40, 90, 60), outline=255, fill=1)  # A button filled
                print("KEY3")

            self._disp.ShowImage(self._disp.getbuffer(image))

            time.sleep(0.1)
