import sys


class ColorPrintNix(object):
    def __init__(self):
        pass

    def red(self, mess, end='\n'):
        sys.stdout.write('\033[31m%s\033[0m' % str(mess+end))
        sys.stdout.flush()

    def green(self, mess, end='\n'):
        sys.stdout.write('\033[32m%s\033[0m' % str(mess+end))
        sys.stdout.flush()

    def yellow(self, mess, end='\n'):
        sys.stdout.write('\033[33m%s\033[0m' % str(mess+end))
        sys.stdout.flush()

    def blue(self, mess, end='\n'):
        sys.stdout.write('\033[34m%s\033[0m' % str(mess+end))
        sys.stdout.flush()

    def pink(self, mess, end='\n'):
        sys.stdout.write('\033[35m%s\033[0m' % str(mess+end))
        sys.stdout.flush()

    def sky_blue(self, mess, end='\n'):
        sys.stdout.write('\033[36m%s\033[0m' % str(mess+end))
        sys.stdout.flush()

    def white(self, mess, end='\n'):
        sys.stdout.write('\033[37m%s\033[0m' % str(mess+end))
        sys.stdout.flush()


if __name__ == '__main__':
    ColorPrintNix().green('DAWN')
