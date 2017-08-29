import re
import sys
import optparse
import glob
import datetime
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
    'version': '3.0.0',
    'update': '2017-8-28',
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
    print '\nPress [Ctrl+Z] to suspend the scanner'
    print '\n'


def florid_get_parse():
    parser = optparse.OptionParser()
    parser.add_option('-u', action='store', dest='url', help='Target URL')
    parser.add_option('-m', action='store', dest='modules', help='Modules to be included')

    (options, args) = parser.parse_args()
    return options


def florid_init(options):
    lib.common.SOURCE_URL = lib.urlentity.URLEntity(options.url).get_url()
    for __file_name in glob.glob('module/phase_one/*.py'):
        if '__init__' not in __file_name and 'pyc' not in __file_name:
            lib.common.MODULE_ONE_NAME_LIST.append(
                re.findall('.*(/|\\\\)(.+)\.py$', __file_name)[0][1])
    if options.modules == 'ALL':
        for __file_name in glob.glob('module/phase_two/*.py'):
            if '__init__' not in __file_name and 'pyc' not in __file_name:
                lib.common.MODULE_NAME_LIST.append(
                    re.findall('.*(/|\\\\)(.+)\.py$', __file_name)[0][1])


def florid_organize():
    core.importer.Importer().import_one()
    core.importer.Importer().import_two()

    tasks = list([])
    # tasks.append(threading.Thread(target=lib.processbar.run, args=()))
    tasks.append(threading.Thread(target=core.producer.Producer(lib.common.SOURCE_URL).run, args=()))
    tasks.append(threading.Thread(target=core.consumer.Consumer().run, args=()))
    tasks.append(threading.Thread(target=core.checker.ResultPrinter().run, args=()))

    for __task in tasks:
        __task.setDaemon(True)
        __task.start()
    for __task in tasks:
        __task.join()

    lib.colorprint.color().green('\n-- FINISH --\n')


if __name__ == '__main__':
    florid_show_banner()
    florid_init(florid_get_parse())
    florid_organize()
