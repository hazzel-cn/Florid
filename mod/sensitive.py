#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import urlparse

import requests

import lib.common as common

if common.WebInfo.os == 'Win':
    import lib.colorprint_win as ColorPrint
else:
    import lib.colorprint_nix as ColorPrint

SVN_DIR = ['wc.db', 'entries']

PHPINFO_FILE = ['1.php', 'phpinfo.php', 'a.php', 'config.php', 'flag.php', '404.php', 'login.php', 'reg.php',
                'view.php']

DIR_LIST = ['admin', 'flag', 'phpmyadmin', 'phpMyAdmin']


def svn_check(url):
    re = ''
    r = requests.get(url + '.svn/')
    if r.status_code == 403:
        re = re + '.svn/'
        for _ in SVN_DIR:
            r = requests.get(url + re + _)
            if r.status_code != 404:
                re = re + _
    ColorPrint.green(re),


def git_check(url):
    re = ''
    r = requests.get(url + '.git/')
    if r.status_code == 403:
        re = re + '.git/'
    ColorPrint.green(re),


def phpinfo_check(url):
    re = ''
    for _ in PHPINFO_FILE:
        r = requests.get(url + '/' + _)
        if r.status_code != 404:
            re = re + ' ' + _

    ColorPrint.green(re),


def dir_check(url):
    re = ''
    for _ in DIR_LIST:
        r = requests.get(url + '/' + _ + '/')
        if r.status_code != 404:
            re = re + ' ' + _
    ColorPrint.green(re),


def init():
    return (True, 'SUCCESS')


def run(url):
    url = url.replace(urlparse.urlparse(url).path.split('/')[-1], '')

    task = []
    task.append(threading.Thread(target=svn_check, args=(url,)))
    task.append(threading.Thread(target=git_check, args=(url,)))
    task.append(threading.Thread(target=phpinfo_check, args=(url,)))
    task.append(threading.Thread(target=dir_check, args=(url,)))

    for _ in task:
        _.start()
    for _ in task:
        _.join()

    '''
    svn_check(url)
    git_check(url)
    phpinfo_check(url)
    '''
    print 'END'
