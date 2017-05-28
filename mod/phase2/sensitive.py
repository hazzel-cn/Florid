#!/usr/bin/python
# -*- coding: utf-8 -*-
# Tips: Only the URLs which the type of is 'D' will be checked here.

import threading

import requests

import lib.colorprint
import lib.common

SVN_DIR = ['wc.db', 'entries']
MODULE_NAME = 'sensitive'


class SvnCheck(object):
    def __init__(self, url_obj):
        self.url_obj = url_obj

    def check(self):
        url_to_be_checked = self.url_obj.value + '.svn/'
        if requests.get(url_to_be_checked).status_code != 404:
            lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['SVN'].append(url_to_be_checked)
            for __file in SVN_DIR:
                if requests.get(url_to_be_checked + __file).status_code != 404:
                    lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['SVN'].append(url_to_be_checked + __file)


class GitCheck(object):
    def __init__(self, url_obj):
        self.url_obj = url_obj

    def check(self):
        if requests.get(self.url_obj.value + '.git/').status_code != 404:
            lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['GIT'].append(self.url_obj.value)


class FileCheck(object):
    def __init__(self, url_obj):
        self.url_obj = url_obj

    def __do_check(self, url):
        try:
            if requests.get(url).status_code != 404:
                lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['FILE'].append(url)
        except:
            try:
                if requests.get(url).status_code != 404:
                    lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['FILE'].append(url)
            except:
                pass

    def check(self):
        tasks = []
        fp = open('./txt/file_set.txt', 'r')
        for __file in fp:
            if __file == '\n':
                continue
            # print self.url_obj.value + __file
            t = threading.Thread(target=self.__do_check, args=(self.url_obj.value + __file.replace('\n', ''), ))
            tasks.append(t)
        for __t in tasks:
            __t.setDaemon(True)
            __t.start()
        for __t in tasks:
            __t.join()


class DirCheck(object):
    def __init__(self, url_obj):
        self.url_obj = url_obj

    def __do_check(self, url):
        try:
            if requests.get(url).status_code != 404:
                lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['DIR'].append(url)
        except:
            try:
                if requests.get(url).status_code != 404:
                    lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['DIR'].append(url)
            except:
                pass

    def check(self):
        tasks = []
        fp = open('./txt/dir_set.txt', 'r')
        for __file in fp:
            if __file == '\n':
                continue
            # print self.url_obj.value[:-1] + __file.replace('\n','')
            t = threading.Thread(target=self.__do_check, args=(self.url_obj.value[:-1] + __file.replace('\n', ''), ))
            tasks.append(t)
        for __t in tasks:
            __t.setDaemon(True)
            __t.start()
        for __t in tasks:
            __t.join()


def init():
    lib.common.RESULT_DIRECROTY[MODULE_NAME].append({})
    lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['FILE'] = []
    lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['GIT'] = []
    lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['SVN'] = []
    lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['DIR'] = []
    return (True, 'SUCCESS')


def run(url_obj):
    current_url_path_list = url_obj.path[1:-1].split('/')
    tmp_new_url = url_obj.source
    tmp_new_url_set = [tmp_new_url]
    for __path_item in current_url_path_list:
        if __path_item != '':
            tmp_new_url = tmp_new_url + __path_item + '/'
            tmp_new_url_set.append(tmp_new_url)

    tasks = []
    for __url in tmp_new_url_set:
        if __url not in lib.common.PATH_SET:
            lib.common.PATH_SET.append(__url)
            __url_obj = lib.urlentity.URLEntity(__url)
            tasks.append(threading.Thread(target=FileCheck(__url_obj).check, args=()))
            tasks.append(threading.Thread(target=GitCheck(__url_obj).check, args=()))
            tasks.append(threading.Thread(target=SvnCheck(__url_obj).check, args=()))
            tasks.append(threading.Thread(target=DirCheck(__url_obj).check, args=()))
    for __t in tasks:
        __t.start()
    for __t in tasks:
        __t.join()
    lib.common.CHECKED_COUNT[MODULE_NAME] += 1
    lib.common.ALL_DOWN_COUNT += 1


if __name__ == '__main__':
    import lib.urlentity

    run(lib.urlentity.URLEntity('www.baozou.com/admin/whoami/inde.php'))
