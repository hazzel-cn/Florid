#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading

import requests

import lib.common as common

if common.WebInfo.os == 'Win':
    import lib.colorprint_win as ColorPrint
else:
    import lib.colorprint_nix as ColorPrint

SVN_DIR = ['wc.db', 'entries']
DIR_LIST = ['/admin/', '/flag/', '/phpmyadmin/', '/phpMyAdmin/', '/wp-admin/']
FILE_LIST = ['.htaccess', '1.php', 'phpinfo.php', 'a.php', 'config.php',
             'flag.php', '404.php', 'login.php', 'reg.php', 'view.php']


def svn_check(url):
    u = common.URL(url)
    re = ''
    check_url = u.value + '.svn/'
    if requests.get(check_url).status_code != 404:
        re = '.SVN/'
        for _ in SVN_DIR:
            if requests.get(check_url + _).status_code != 404:
                re = re + _ + ' '
    ColorPrint.green(re),


def git_check(url):
    u = common.URL(url)
    if requests.get(u.value + '.git/').status_code != 404:
        ColorPrint.green('.GIT/'),


def file_check(url):
    u = common.URL(url)
    for _ in FILE_LIST:
        if requests.get(u.value + _).status_code != 404:
            ColorPrint.green(_),


def dir_check(url):
    u = common.URL(url)
    for _ in DIR_LIST:
        if requests.get(u.value + _[1:]).status_code != 404:
            ColorPrint.green(_),


def init():
    return (True, 'SUCCESS')


def run(url):
    u_obj = common.URL(url)
    tmp_path_list = u_obj.path[1:-1].split('/')
    tmp_full_path_list = []
    tmp_url = u_obj.netloc + '/'
    for i in xrange(len(tmp_path_list)):
        tmp_url = tmp_url + tmp_path_list[i] + '/'
        tmp_full_path_list.append(tmp_url)

    task = []
    for _u in tmp_full_path_list:
        if _u not in common.SENSITIVE_LIST:
            if common.URL(_u).type == 'D':
                common.SENSITIVE_LIST.append(_u)
                task.append(threading.Thread(target=svn_check, args=(_u,)))
                task.append(threading.Thread(target=git_check, args=(_u,)))
                task.append(threading.Thread(target=dir_check, args=(_u,)))
                task.append(threading.Thread(target=file_check, args=(_u,)))

    for _ in task:
        _.start()
    for _ in task:
        _.join()

    print 'END'
