#!/usr/bin/python3
""" Manage OLED 128x32 display light """

# MIT License
#
# Copyright (c) 2019 Dave Wilson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# pylint: disable=bad-whitespace
# pylint: disable=too-many-public-methods

import Adafruit_SSD1306

FONT = "/home/an/diyid/Tahoma.ttf"
FONT_SIZE = 13

class DiyOLED128x64:
    """ OLED display 128 by 64 """

    def __init__(self,):
        """ Initialize the VCNL40xx sensor """
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)
        self.disp.begin()
        self.disp.clear()
        # Create image buffer. Make sure to create image with mode '1' for 1-bit color.
        self.image = Image.new('1', (self.disp.width, self.disp.height))
        self.font = ImageFont.truetype(FONT, FONT_SIZE)
        # Some nice fonts to try: http://www.dafont.com/bitmap.php
        self.draw = ImageDraw.Draw( self.image )
        self.line = ["0", "1", "2", "3", "4"]

    def reset(self,):
        """ reset the device to the default condition """
        self.disp.clear()
        self.disp.display()
        self.line = ["0", "1", "2", "3", "4"]

    def set(self, line=0, val=""):
        """ set the specified line with text which will be displayed on show() """
        if line >= 0:
            if line <= 4:
                self.line[line] = val

    def show(self,):
        """ clear and display 3 lines of text """
        self.disp.clear()
        self.draw.rectangle((0,0,self.disp.width,self.disp.height), outline=0, fill=0)
        for x in range(4):
            row = (x*(FONT_SIZE+2))
            self.draw.text((0,row),  self.line[x], font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

    def clear(self,):
        """ clear display """
        self.disp.clear()
        self.disp.display()

if __name__ == '__main__':
    exit()

