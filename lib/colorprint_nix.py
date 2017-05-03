# coding=utf-8
import sys


class ColorPrintNix(object):
    def __init__(self):
        pass

    def red(self, mess):
        sys.stdout.write('\033[31m%s\033[0m' % str(mess))

    def green(self, mess):
        sys.stdout.write('\033[32m%s\033[0m' % str(mess))

    def yellow(self, mess):
        sys.stdout.write('\033[33m%s\033[0m' % str(mess))

    def blue(self, mess):
        sys.stdout.write('\033[34m%s\033[0m' % str(mess))

    def pink(self, mess):
        sys.stdout.write('\033[35m%s\033[0m' % str(mess))

    def sky_blue(self, mess):
        sys.stdout.write('\033[36m%s\033[0m' % str(mess))

    def white(self, mess):
        sys.stdout.write('\033[37m%s\033[0m' % str(mess))


if __name__ == '__main__':
    ColorPrintNix().green('DAWN')
