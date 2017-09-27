import datetime
import glob
import optparse
import re
import signal
import sys
import threading

import core.initializer

core.initializer.Initializer().init()

import lib.common
import lib.colorprint
import lib.processbar
import lib.urlentity
import core.importer
import core.producer
import core.consumer
import core.checker

reload(sys)
sys.setdefaultencoding('utf8')

florid_banner = {
    'version': '3.2.4',
    'update': '2017-9-25',
    'logo':
        r'''
         _______         _____   ______ _____ ______ 
         |______ |      |     | |_____/   |   |     \
         |       |_____ |_____| |    \_ __|__ |_____/
        '''
}


def florid_show_banner():
    lib.colorprint.color().pink(florid_banner['logo'])
    print '[Florid Version] ' + florid_banner['version']
    print '[Last Updated] ' + florid_banner['update']
    print '[*] ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print '\nPress [Ctrl+C] to abort the scan'
    print '\n'


def florid_get_parse():
    parser = optparse.OptionParser()
    parser.add_option('-u', action='store', dest='url', help='Target URL')
    parser.add_option('-m', action='store', dest='modules', help='Modules to be included')

    (options, args) = parser.parse_args()

    if options.modules is None:
        lib.colorprint.color().red('[!] Fatal Error: No modules specified. Use "-m" to do it.', end='\n')
        lib.colorprint.color().red('[!] You can get help with "-h"', end='\n')
        exit()
    return options


def florid_init(options):
    lib.common.SOURCE_URL = lib.urlentity.URLEntity(options.url).get_url()
    for __file_name in glob.glob('module/phase_one/*.py'):
        if '__init__' not in __file_name and 'pyc' not in __file_name:
            lib.common.MODULE_ONE_NAME_LIST.append(
                re.findall('.*(/|\\\\)(.+)\.py$', __file_name)[0][1])
    if options.modules.lower() == 'all':
        for __file_name in glob.glob('module/phase_two/*.py'):
            if '__init__' not in __file_name and 'pyc' not in __file_name:
                lib.common.MODULE_NAME_LIST.append(
                    re.findall('.*(/|\\\\)(.+)\.py$', __file_name)[0][1])
    else:
        if options.modules != '':
            for __file_name in options.modules.replace(' ', '').split(','):
                lib.common.MODULE_NAME_LIST.append(__file_name)


def florid_organize():
    core.importer.Importer().do_import()

    tasks = list([])
    # tasks.append(threading.Thread(target=lib.processbar.run, args=()))
    tasks.append(threading.Thread(target=core.producer.Producer(lib.common.SOURCE_URL).run, args=()))
    tasks.append(threading.Thread(target=core.consumer.Consumer().run, args=()))
    tasks.append(threading.Thread(target=core.checker.ResultPrinter().run, args=()))

    for __task in tasks:
        __task.setDaemon(True)
        __task.start()
    while not lib.common.FLAG['scan_done']:
        alive = False
        if lib.common.FLAG['stop_signal']:
            for t in tasks:
                alive = alive or t.isAlive()
            if not alive:
                break

    lib.colorprint.color().green('\n-- FINISH --\n')


def florid_exit(signum, frame):
    lib.common.FLAG['stop_signal'] = True
    lib.colorprint.color().red('\n\n[!] User abort. Terminating the scan...')


if __name__ == '__main__':
    signal.signal(signal.SIGINT, florid_exit)
    signal.signal(signal.SIGTERM, florid_exit)
    florid_show_banner()
    florid_init(florid_get_parse())
    florid_organize()
