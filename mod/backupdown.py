#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import threading

import requests

import lib.common as common

if common.WebInfo.os == 'Win':
    import lib.colorprint_win as ColorPrint
else:
    import lib.colorprint_nix as ColorPrint

MODULE_NAME = 'backupdown'
SUFFIX_ARRAY = ['.swp', '.swo', '.swn', '.swp4']
INCLUDED_SUFFIX = ['.php', '.asp']


def do_vim_down(url, filename, suffix):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code != 404:
            fp = open(common.LOG_DICT + filename + suffix, 'wb')
            fp.write(r.content)
            fp.close()
            ColorPrint.green('VIM ')
            sys.stdout.flush()
    except:
        pass


def vim_down(u_obj):
    for suffix in SUFFIX_ARRAY:
        url_down = u_obj.scheme + '://' + u_obj.netloc + u_obj.path + '.' + u_obj.filename + suffix
        t = threading.Thread(target=do_vim_down, args=(url_down, u_obj.filename, suffix))
        t.start()
        t.join()


def gedit_down(u_obj):
    url_down = u_obj.scheme + '://' + u_obj.netloc + u_obj.path + u_obj.filename + '~'
    try:
        r = requests.get(url_down)
        if r.status_code != 404:
            _f = open(common.LOG_DICT + u_obj.filename + '~', 'wb')
            _f.write(r.content)
            ColorPrint.green('GEDIT ')
            sys.stdout.flush()
            return True
    except:
        pass


def back_down(u_obj):
    url_down = u_obj.scheme + '://' + u_obj.netloc + u_obj.path + u_obj.filename + '.bak'
    try:
        r = requests.get(url_down)
        if r.status_code != 404:
            _f = open(common.LOG_DICT + u_obj.filename + '.bak', 'wb')
            _f.write(r.content)
            ColorPrint.green('BAK ')
            sys.stdout.flush()
            return True
    except:
        pass


def init():
    return (True, 'SUCCESS')


def run(url):
    u_obj = common.URL(url)
    if u_obj.type == 'F' and u_obj.value not in common.BACKUPDOWN_LIST:
        common.BACKUPDOWN_LIST.append(u_obj.value)
        if '.' + u_obj.filename.split('.')[-1].lower() in INCLUDED_SUFFIX:
            task = []
            task.append(threading.Thread(target=vim_down, args=(u_obj,)))
            task.append(threading.Thread(target=gedit_down, args=(u_obj,)))
            task.append(threading.Thread(target=back_down, args=(u_obj,)))
            for _ in task:
                _.start()
            for _ in task:
                _.join()
    return True
