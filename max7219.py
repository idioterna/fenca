# The MIT License (MIT)
#
# Copyright (c) 2016 Radomir Dopieralski
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

_NOOP = const(0)
_DIGIT0 = const(1)
_DIGIT1 = const(2)
_DIGIT2 = const(3)
_DIGIT3 = const(4)
_DIGIT4 = const(5)
_DIGIT5 = const(6)
_DIGIT6 = const(7)
_DIGIT7 = const(8)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)

_D = [
    0x7e,
    0x30,
    0x6d,
    0x79,
    0x33,
    0x5b,
    0x5f,
    0x70,
    0x7f,
    0x7b,
]


class Matrix8x8:
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.cs.init(cs.OUT, True)
        self.buffer = bytearray(8)
        self.init()

    def _register(self, command, data):
        self.cs.value(0)
        self.spi.write(bytearray([command, data]))
        self.cs.value(1)

    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._register(command, data)

    def brightness(self, value):
        if not 0<= value <= 15:
            raise ValueError("Brightness out of range")
        self._register(_INTENSITY, value)

    def fill(self, color):
        data = 0xff if color else 0x00
        for y in range(8):
            self.buffer[y] = data

    def pixel(self, x, y, color=None):
        if color is None:
            return bool(self.buffer[y] & 1 << x)
        elif color:
            self.buffer[y] |= 1 << x
        else:
            self.buffer[y] &= ~(1 << x)

    def show(self):
        for y in range(8):
            self._register(_DIGIT0 + y, self.buffer[y])

    def dot(self, pos, on=1):
        if on:
            self.buffer[pos] |= 0x80
        else:
            self.buffer[pos] &= 0x7f

    def digit(self, x, digit, dot=0):
        self.buffer[x] = _D[digit]
        if dot: self.buffer[x] |= 0x80

    def nprint(self, number, pad=False):
        if not isinstance(number, str):
            raise ValueError("Pass number as a string")
        pos = 0
        dot = 0
        for digit in reversed(number):
            if digit == '.':
                dot = 1
                continue
            else:
                self.digit(pos, int(digit), dot)
                dot = 0
            pos += 1
        while pad and pos < 8:
            self.digit(pos, 0)
            pos += 1

    def p(self, n):
        self.fill(0)
        self.nprint(str(n))
        self.show()

