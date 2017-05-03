# coding=utf-8

import ctypes
import sys

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

FOREGROUND_BLACK = 0x00  # black.
FOREGROUND_DARKBLUE = 0x01  # dark blue.
FOREGROUND_DARKGREEN = 0x02  # dark green.
FOREGROUND_DARKSKYBLUE = 0x03  # dark skyblue.
FOREGROUND_DARKRED = 0x04  # dark red.
FOREGROUND_DARKPINK = 0x05  # dark pink.
FOREGROUND_DARKYELLOW = 0x06  # dark yellow.
FOREGROUND_DARKWHITE = 0x07  # dark white.
FOREGROUND_DARKGRAY = 0x08  # dark gray.
FOREGROUND_BLUE = 0x09  # blue.
FOREGROUND_GREEN = 0x0a  # green.
FOREGROUND_SKYBLUE = 0x0b  # skyblue.
FOREGROUND_RED = 0x0c  # red.
FOREGROUND_PINK = 0x0d  # pink.
FOREGROUND_YELLOW = 0x0e  # yellow.
FOREGROUND_WHITE = 0x0f  # white.

std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool


# reset white
def reset_color():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)


class ColorPrintWin(object):
    def __init__(self):
        pass

    def blue(self, mess):
        set_cmd_text_color(FOREGROUND_BLUE)
        sys.stdout.write(mess)
        sys.stdout.flush()
        reset_color()

    def green(self, mess):
        set_cmd_text_color(FOREGROUND_GREEN)
        sys.stdout.write(mess)
        sys.stdout.flush()
        reset_color()

    def sky_blue(self, mess):
        set_cmd_text_color(FOREGROUND_SKYBLUE)
        sys.stdout.write(mess)
        sys.stdout.flush()
        reset_color()

    def red(self, mess):
        set_cmd_text_color(FOREGROUND_RED)
        sys.stdout.write(mess)
        sys.stdout.flush()
        reset_color()

    def pink(self, mess):
        set_cmd_text_color(FOREGROUND_PINK)
        sys.stdout.write(mess)
        sys.stdout.flush()
        reset_color()

    def yellow(self, mess):
        set_cmd_text_color(FOREGROUND_YELLOW)
        sys.stdout.write(mess)
        sys.stdout.flush()
        reset_color()

    def white(self, mess):
        set_cmd_text_color(FOREGROUND_WHITE)
        sys.stdout.write(mess)
        sys.stdout.flush()
        reset_color()


if __name__ == '__main__':
    ColorPrintWin().green('DAWN')
