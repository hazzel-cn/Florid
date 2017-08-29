# coding=utf-8
import sys
import time

import lib.colorprint
import lib.common


class ProgressBar:
    def __init__(self, count=0, total=0, width=50):
        self.count = count
        self.total = total
        self.width = width

    def log(self, _sign):
        count = lib.common.ALL_DOWN_COUNT
        sys.stdout.write(' ' * (self.width + 10) + '\r')
        sys.stdout.flush()
        lib.colorprint.color().green('[RUNNING] ' + _sign + ' ' + '>' * (count % 15) + '\r')
        sys.stdout.flush()


def run():
    count = 0
    while not lib.common.FLAG['scan_done']:
        a_side = ['\\', '|', '/', '-']
        b_side = 'floooooooooooooorid'
        i = count % len(b_side)
        n = b_side[:i] + chr(ord(b_side[i])-32) + b_side[i+1:]
        lib.colorprint.color().green('__' + a_side[count % 4] + '__' + n, end='\r')
        time.sleep(0.1)
        count += 1
