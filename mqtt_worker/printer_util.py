import six
from escpos.constants import *

class PrinterUtil():
    def __init__(self, printer):
        self._printer = printer

    def init(self):
        command = ESC + b'@'
        self._printer._raw(command)

    # use this method to print Chinese characters correctly:
    # pu.text("Hello129你好\n".encode('GB18030'))
    def text(self, text):
        self._printer._raw(text)
        self._printer._raw(CTL_CR + CTL_LF)

    def test_page(self):
        command = b'\x12' + b'T'
        self._printer._raw(command)

    # IMPORTANT:
    # should be set before other settings
    def bold(self, bold = True):
        command = ESC + b'!' + (b'\x08' if bold else b'\x00')
        self._printer._raw(command)

    def double_width(self, double_width = True):
        command = ESC + (b'\x0E' if double_width else b'\x14')
        self._printer._raw(command)

    # 12x24
    def font_a(self):
        command = ESC + b'!' + b'\x00'
        self._printer._raw(command)

    # 9x17
    def font_b(self):
        command = ESC + b'!' + b'\x01'
        self._printer._raw(command)
    
    # 1~8
    def font_size(self, width_scale = 1, height_scale = 1):
        if width_scale < 1 or width_scale > 8 or height_scale < 1 or height_scale > 8:
            return
        command = GS + b'!' + six.int2byte(((width_scale - 1) << 4) + (height_scale - 1))
        self._printer._raw(command)

    def invert_color(self, invert = True):
        command = GS + b'B' + (b'\x01' if invert else b'\x00')
        self._printer._raw(command)

    def rotate(self, rotate = True):
        command = ESC + b'V' + (b'\x01' if rotate else b'\x00')
        self._printer._raw(command)

    def rotate_180(self, rotate = True):
        command = ESC + b'{' + (b'\x01' if rotate else b'\x00')
        self._printer._raw(command)

