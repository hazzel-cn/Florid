#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading

import requests

import lib.common as common

if common.WebInfo.os == 'Windows':
    import lib.colorprint_win as ColorPrint
else:
    import lib.colorprint_nix as ColorPrint

SVN_DIR = ['wc.db', 'entries']


def svn_check(u):
    re = ''
    check_url = u.value + '.svn/'
    if requests.get(check_url).status_code != 404:
        re = '.SVN/'
        for _ in SVN_DIR:
            if requests.get(check_url + _).status_code != 404:
                re = re + _ + ' '
    ColorPrint.green(re),


def git_check(u):
    if requests.get(u.value + '.git/').status_code != 404:
        ColorPrint.green('.GIT/'),


def file_check(u):
    fp = open('./txt/file_set.txt', 'r')
    for _ in fp:
        if _ == '\n':
            continue
        t = threading.Thread(target=check_and_print, args=(u.value, _.replace('\n', ''), u.path))
        t.setDaemon(True)
        t.start()
    fp.close()


def dir_check(u):
    fp = open('./txt/dir_set.txt', 'r')
    for _ in fp:
        if _ == '\n':
            continue
        t = threading.Thread(target=check_and_print, args=(u.value, _.replace('\n', ''), u.path))
        t.setDaemon(True)
        t.start()
        t.join()
    fp.close()


def check_and_print(head, tail, path):
    if tail.startswith('/'):
        req_u = head + tail[1:]
    else:
        req_u = head + tail

    if requests.get(req_u).status_code != 404:
        ColorPrint.green(path + tail + '  ')
        sys.stdout.flush()


def init():
    return (True, 'SUCCESS')


def run(url):
    u_obj = common.URL(url)
    tmp_path_list = u_obj.path[1:-1].split('/')
    tmp_url = u_obj.netloc + '/'
    tmp_full_path_list = [tmp_url]

    while '' in tmp_path_list:
        tmp_path_list.remove('')

    if len(tmp_path_list) > 0:
        for _path in tmp_path_list:
            tmp_url = tmp_url + _path + '/'
            tmp_full_path_list.append(tmp_url)

    task = []
    for _u in tmp_full_path_list:
        if _u not in common.SENSITIVE_LIST:
            if common.URL(_u).type == 'D':
                common.SENSITIVE_LIST.append(_u)
                _u_obj = common.URL(_u)
                task.append(threading.Thread(target=svn_check, args=(_u_obj,)))
                task.append(threading.Thread(target=git_check, args=(_u_obj,)))
                task.append(threading.Thread(target=dir_check, args=(_u_obj,)))
                task.append(threading.Thread(target=file_check, args=(_u_obj,)))

    for _ in task:
        _.start()
    for _ in task:
        _.join()

    return True
