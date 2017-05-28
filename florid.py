import datetime
import glob
import optparse
import re
import sys
import threading

import core.checker
import core.distributor
import core.helper
import core.importer
import core.prepare
import core.spider
import lib.common
import lib.processbar

reload(sys)
sys.setdefaultencoding('utf8')
sys.dont_write_bytecode = True

florid_banner = {
    'version': '2.2.0 dev',
    'update': '2017-05-21',
    'logo': '''
     _____  _            _     _
    |  ___|| | ___  _ __(_) __| |
    | |__  | |/ _ \| '__| |/ _` |
    |  __| | | (_) | |  | | (_| |
    |_|    |_|\___/|_|  |_|\__,_| [ CTF ACTIVE SCANNER ]
    '''
}


def florid_show_banner():
    print florid_banner['logo']
    print '[Florid Version] ' + florid_banner['version']
    print '[Last Updated] ' + florid_banner['update']
    print '[*] ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print '\n'


def florid_get_parse():
    parser = optparse.OptionParser()
    parser.add_option('-u', action='store', dest='url', help='Target URL')
    parser.add_option('-m', action='store', dest='modules', help='Modules to be included')
    parser.add_option('-v', action='store_true', dest='verbose', help='Flag to show details')

    (options, args) = parser.parse_args()
    return options


def florid_init(options):
    # The URL to be checked at first
    lib.common.SOURCE_URL = options.url

    if options.modules == 'ALL':
        for __file_name in glob.glob('mod/phase2/*.py'):
            if '__init__' not in __file_name and 'pyc' not in __file_name:
                # print __file_name, re.findall('.*(/|\\\\)(.+)\.py$', __file_name)[0][1]
                # exit()
                lib.common.COMMAND_SET['module_list'].append(
                    re.findall('.*(/|\\\\)(.+)\.py$', __file_name)[0][1])


def florid_organize():
    if lib.common.OS == 'WIN':
        import os
        core.helper.WatcherWin(os.getpid())
    else:
        core.helper.WatcherNix()

    # Run modules for phase one:
    core.prepare.import_modules_phase_one()
    core.prepare.run_modules_phase_one()

    # Import modules for phase two:
    core.importer.import_modules_phase_two()

    # Start Spider to crawl the website
    t_spider = threading.Thread(target=core.spider.Spider(lib.common.SOURCE_URL).run, args=())
    # Start the distributor to distribute the URL to various modules
    t_distributor = threading.Thread(target=core.distributor.consume, args=())
    # Start the process bar
    t_processbar = threading.Thread(target=lib.processbar.run, args=())
    # Start the checker to show result every time a module has checked all urls
    t_checker = threading.Thread(target=core.checker.run, args=())

    t_processbar.setDaemon(True)
    t_processbar.start()

    t_checker.start()

    t_spider.start()
    t_distributor.start()
    t_spider.join()
    t_distributor.join()

    t_checker.join()
    lib.common.SCAN_DONE_FLAG = True


def main():
    florid_show_banner()
    florid_init(florid_get_parse())
    florid_organize()
    print '\n[!] Finished.\n'
    exit()


if __name__ == '__main__':
    main()
