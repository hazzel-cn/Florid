#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import glob
import optparse
import os
import platform
import sys
import threading

import lib.common as common
import lib.helper as helper
import mod.spider

if common.WebInfo.os == 'Windows':
    import lib.colorprint_win as ColorPrint
else:
    import lib.colorprint_nix as ColorPrint

sys.dont_write_bytecode = True

florid_banner = {
    'version': '0.3.4 dev',
    'update': '2017-03-13',
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


def florid_init_env(options):
    common.WebInfo.os = platform.system()

    # target URL
    common.WebInfo.url = ''
    if options.url is not None:
        if not options.url.startswith('http'):
            common.WebInfo.url = 'http://' + options.url
        else:
            common.WebInfo.url = options.url

    # Modules array
    common.WebInfo.modules = []
    if options.modules is not None:
        common.WebInfo.modules = options.modules.replace(' ', '').split(',')

    # Verbose
    common.WebInfo.verbose = options.verbose

    return common.WebInfo


def florid_import_modules():
    if common.WebInfo.modules is None:
        return False
    # Load modules list
    if 'ALL' in common.WebInfo.modules:
        common.WebInfo.modules.remove('ALL')
        for __module in glob.glob('mod/*.py'):
            if '__init__' not in __module:
                common.WebInfo.modules.append(__module[4:].replace('.py', ''))
        common.WebInfo.modules.remove('spider')
        common.WebInfo.modules.remove('sqli')
    # Import modules from the list above && initialize every module
    print '__MODS__'
    for _ in common.WebInfo.modules:
        print '\t\_%s\t' % _,
        try:
            _m = __import__('mod.' + _, fromlist=["*.py"])
            _m_init_result = _m.init()
            if _m_init_result[0]:
                ColorPrint.green(_m_init_result[1] + '\n')
                common.WebInfo.modules_list[_] = _m
            else:
                ColorPrint.red(_m_init_result[1])
                continue
        except:
            pass
    print '\n'
    return common.WebInfo.modules_list


def spider_module_call():
    import mod.spider
    threading.Thread(target=mod.spider.run, args=()).start()


def sqli_module_call():
    import mod.sqli
    mod.sqli.init()
    mod.sqli.run(common.WebInfo.url)


def other_modules_call():
    while not common.SPIDER_END or common.TASK_QUEUE.qsize() > 0:
        if common.LOCKER.acquire():
            if common.TASK_QUEUE.qsize() > 0:
                url = common.TASK_QUEUE.get()
                print '\n\tChecking... + %s' % url
                for _ in common.WebInfo.modules_list:
                    print '\t\t|_',
                    ColorPrint.sky_blue(_)
                    print ' is running......\t',
                    _t = threading.Thread(target=common.WebInfo.modules_list[_].run, args=(url,))
                    _t.start()
                    _t.join()
                    print '[END]'
                common.LOCKER.release()
            else:
                common.LOCKER.wait()


def main():
    florid_show_banner()
    florid_init_env(florid_get_parse())

    florid_import_modules()
    if common.WebInfo.os == 'Windows':
        helper.Watcher_Windows(os.getpid())
    else:
        helper.Watcher_Linux()
    threading.Thread(target=mod.spider.run, args=()).start()
    threading.Thread(target=other_modules_call, args=()).start()


if __name__ == '__main__':
    main()
