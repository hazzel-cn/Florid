#!/usr/bin/python
# -*-coding:utf-8-*-
import glob


MODULE_NAME = 'All Modules'


def run(options):
    module_list = []
    for __module in glob.glob('mod/*.py'):
        if '__init__' not in __module and 'A' not in __module:
            __module = __module.replace('/', '.').replace('.py', '')
            try:
                print '[+] Importing Module \033[33m' + __module.replace('mod.', '') + '\033[0m...\t',
                m = __import__(__module, fromlist=["*"])
                module_list.append(m)
                print '\033[32m[^] Done \033[0m'
            except:
                print '\033[31m[!] Fail\033[0m'
    print '\n'
    for __module in module_list:
        print '\n(\033[36m' + __module.MODULE_NAME + '\033[0m)\t>>======'
        __module.run(options)


#
# http://blog.csdn.net/pi9nc/article/details/26750487