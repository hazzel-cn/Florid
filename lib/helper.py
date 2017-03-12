import os
import signal
import sys

import lib.common as common

if common.WebInfo.os == 'Win':
    import lib.colorprint_win as ColorPrint
else:
    import lib.colorprint_nix as ColorPrint


class Watcher():
    def __init__(self):
        self.child = os.fork()
        if self.child == 0:
            return
        else:
            self.watch()

    def watch(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            print '\n\n'
            ColorPrint.red('[!] User Abort')
            print '\n\n'
            self.kill()
        sys.exit()

    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError:
            pass
