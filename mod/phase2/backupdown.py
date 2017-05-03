#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import requests
import lib.common
import lib.colorprint

MODULE_NAME = str(__file__).split('/')[-1].split('\\')[-1].replace('.pyc', '').replace('.py', '')
SUFFIX_ARRAY = ['.swp', '.swo', '.swn', '.swp4']
INCLUDED_SUFFIX = ['.php', '.asp']
CHECKED_URL_OBJ_SET = []


class VimDown(object):
    def __init__(self, url_obj):
        self.url_obj = url_obj

    def __download(self, suffix):
        url_to_be_checked = \
            self.url_obj.body.replace(self.url_obj.filename, '.' + self.url_obj.filename) + suffix
        try:
            r = requests.get(url_to_be_checked, timeout=3)
            if r.status_code != 404:
                lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['VIM'].append(self.url_obj.body)
                CHECKED_URL_OBJ_SET.append(self.url_obj.value.replace(self.url_obj.filename, ''))
                __logfile = open('log/' + self.url_obj.hostname + '/' + self.url_obj.filename + suffix, 'wb')
                __logfile.writelines(r.content)
                return True
            else:
                pass
        except Exception, e:
            pass

    def download(self):
        tasks = []
        for __suffix in SUFFIX_ARRAY:
            tasks.append(threading.Thread(target=self.__download, args=(__suffix,)))
        for t in tasks:
            t.start()
        for t in tasks:
            t.join()
        return False


class GeditDown(object):
    def __init__(self, url_obj):
        self.url_obj = url_obj

    def download(self):
        url_to_be_checked = self.url_obj.body + '~'
        try:
            r = requests.get(url_to_be_checked)
            if r.status_code != 404:
                __logfile = open('log/' + self.url_obj.hostname + '/' + self.url_obj.filename + '~', 'wb')
                __logfile.writelines(r.content)
                CHECKED_URL_OBJ_SET.append(self.url_obj.value.replace(self.url_obj.filename, ''))
                lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['Gedit'].append(url_to_be_checked)
                return True
            else:
                pass
        except Exception, e:
            pass
        return False


class BackDown(object):
    def __init__(self, url_obj):
        self.url_obj = url_obj

    def download(self):
        url_to_be_checked = self.url_obj.body + '.bak'
        try:
            r = requests.get(url_to_be_checked)
            if r.status_code != 404:
                lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['General'].append(url_to_be_checked)
                CHECKED_URL_OBJ_SET.append(self.url_obj.value.replace(self.url_obj.filename, ''))
                __logfile = open('log/' + self.url_obj.hostname + '/' + self.url_obj.filename + '.bak', 'wb')
                __logfile.writelines(r.content)
                return True
            else:
                pass
        except Exception, e:
            pass
        return False


def init():
    lib.common.RESULT_DIRECROTY[MODULE_NAME].append({})
    lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['VIM'] = []
    lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['Gedit'] = []
    lib.common.RESULT_DIRECROTY[MODULE_NAME][0]['General'] = []
    return (True, 'SUCCESS')


def run(url_obj):

    suffix = '.' + url_obj.filename.split('.')[-1].lower()
    if url_obj.type == 'F' and suffix in INCLUDED_SUFFIX:
        if url_obj.filename.replace(url_obj.filename, '') not in CHECKED_URL_OBJ_SET:
            task = []
            task.append(threading.Thread(target=VimDown(url_obj).download, args=()))
            task.append(threading.Thread(target=GeditDown(url_obj).download, args=()))
            task.append(threading.Thread(target=BackDown(url_obj).download, args=()))

            for t in task:
                t.start()
            for t in task:
                t.join()
    lib.common.CHECKED_COUNT[MODULE_NAME] += 1
    lib.common.ALL_DOWN_COUNT += 1



if __name__ == '__main__':
    init()
    import lib.urlentity

    url = '115.159.210.46/test.php'
    url_obj = lib.urlentity.URLEntity(url)
    VimDown(url_obj).download()
