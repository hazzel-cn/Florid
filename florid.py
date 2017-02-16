#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
import time
import optparse
import datetime

florid = {
    'version': '0.1 dev',
    'update': '2017-02-15',
    'logo': '''
     _____  _            _     _
    |  ___|| | ___  _ __(_) __| |
    | |__  | |/ _ \| '__| |/ _` |
    |  __| | | (_) | |  | | (_| |
    |_|    |_|\___/|_|  |_|\__,_| [ ACTIVE SCANNER ]
    '''
}


def show_banner():
    print florid['logo']
    print '[Florid Version] ' + florid['version']
    print '[Last Updated] ' + florid['update']
    print '[*] ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print '\n'


def get_parser():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--url', action = 'store', dest = 'url', help = 'The URL you want to scan')
    parser.add_option('-f', '--file', action = 'store', dest = 'file', help = 'The file containing URLs')
    parser.add_option('-m', '--module', action = 'store', dest = 'module', help = 'Module names (split with ",")')
    parser.add_option('-t', '--stime', action = 'store', dest = 'stime', type = 'int', default = 0, help = 'Sleep time')
    (options, args) = parser.parse_args()
    if options.url is not None and '://' not in options.url:
        options.url = 'http://' + options.url
    if options.module is not None:
        options.module = options.module.split(',')
        print '[*] Scanning the\033[33m {0}\033[0m with module{1}'.format(options.url, ','.join('\033[33m ' + _ + '\033[0m' for _ in options.module))
    return options


def load_module(module):
    if module is None:
        return False
    real_module = []
    for _ in module:
        try:
            print '[+] Importing Module \033[33m' + _ + '\033[0m...\t',
            m = __import__('mod.' + _, fromlist = ["*"])
            real_module.append(m)
            print '\033[32m[^] Done \033[0m'
        except:
            print '\033[31m[!] Fail\033[0m'
    return real_module


def main():
    show_banner()
    options = get_parser()
    options.module = load_module(options.module)

    if options.module is not False:
        for _ in options.module:
            print '\n(\033[34m' + _.MODULE_NAME + '\033[0m)\t>>======'
            _.run(options)


if __name__ == '__main__':
    main()