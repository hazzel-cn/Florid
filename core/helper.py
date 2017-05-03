import os
import signal
import sys
import time
import multiprocessing
import lib.colorprint


class WatcherNix():
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
            lib.colorprint.color().red('[!] User Abort')
            print '\n\n'
            self.kill()
        sys.exit()

    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError:
            pass


class WatcherWin():
    def __init__(self, pid):
        self.pid = pid
        multiprocessing.Process(target=self.watch, args=()).start()

    def watch(self):
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print '\n\n'
            lib.colorprint.color().red('[!] User Abort')
            print '\n\n'
            self.kill()
        sys.exit()

    def kill(self):
        try:
            os.system('taskkill /F /pid ' + str(self.pid))
        except:
            pass
