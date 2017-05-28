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
    bar = ProgressBar(total=10)

    while not lib.common.SCAN_DONE_FLAG:
        for _sign in ['\\', '|', '/', '-']:
            bar.log(_sign)
            time.sleep(0.1)
