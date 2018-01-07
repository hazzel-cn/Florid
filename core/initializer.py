import imp
import os
import platform
import time

import lib.common

NEEDED_MODULES = ['requests', 'bs4']


class Initializer:
    def __init__(self):
        self.__uninstalled_modules_list = list()

    def __os_init(self):
        lib.common.CONFIG['OS_type'] = 'WIN' if platform.system() == 'Windows' else 'NIX'

    def __time_init(self):
        lib.common.CONFIG['time:'] = time.localtime(time.time())

    def __modules_init(self):
        # Dict is for the storage of the status of needed modules
        for needed_module in NEEDED_MODULES:
            try:
                imp.find_module(needed_module)
            except ImportError:
                self.__uninstalled_modules_list.append(needed_module)
        if len(self.__uninstalled_modules_list) > 0:
            print '[!] Some necessary modules are needed:'
            for needed_module in self.__uninstalled_modules_list:
                print '\t* %s' % needed_module
            raw_input('Press [Enter] to install them.')
            for needed_module in self.__uninstalled_modules_list:
                os.system('pip install %s' % needed_module)
            if lib.common.CONFIG['OS_type'] == 'WIN':
                os.system('cls')
            else:
                os.system('clear')

    def init(self):
        self.__os_init()
        self.__time_init()
        self.__modules_init()
        return True


if __name__ == '__main__':
    init = Initializer().init()
