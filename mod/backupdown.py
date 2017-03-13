#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import threading
import urlparse

import requests

import lib.common as common

if common.WebInfo.os == 'Win':
    import lib.colorprint_win as ColorPrint
else:
    import lib.colorprint_nix as ColorPrint

MODULE_NAME = 'backupdown'
SUFFIX_ARRAY = ['.swp', '.swo', '.swn', '.swp4']
INCLUDED_SUFFIX = ['.php', '.asp']


class VimDown(object):
    def __init__(self, check_url):
        self.check_url = check_url
        self.ob = urlparse.urlparse(self.check_url)
        self.scheme = self.ob.scheme
        self.hostname = self.ob.hostname
        self.dirname = os.path.dirname(self.check_url)
        self.basename = os.path.basename(self.check_url).replace(urlparse.urlparse(self.check_url).query, '').replace(
            '?', '')

    def download(self):
        for _ in SUFFIX_ARRAY:
            url_down = self.dirname + '/.' + self.basename + _
            try:
                r = requests.get(url_down, timeout=3)
                if r.status_code == 200:
                    _f = open('log/' + self.hostname + '/' + self.basename + _, 'wb')
                    _f.write(r.content)
                    ColorPrint.green('VIM')
                    return True
                else:
                    pass
            except:
                pass
        return False


class GeditDown(object):
    def __init__(self, check_url):
        self.check_url = check_url
        self.ob = urlparse.urlparse(self.check_url)
        self.scheme = self.ob.scheme
        self.hostname = self.ob.hostname
        self.dirname = os.path.dirname(self.check_url)
        self.basename = os.path.basename(self.check_url).replace(urlparse.urlparse(self.check_url).query, '').replace(
            '?', '')

    def download(self):
        url_down = self.check_url + '~'
        try:
            r = requests.get(url_down)
            if r.status_code == 200:
                _f = open('log/' + self.hostname + '/' + self.basename + '~', 'wb')
                _f.write(r.content)
                ColorPrint.green('GEDIT')
                return True
            else:
                pass
        except:
            pass
        return False


def init():
    return (True, 'SUCCESS')


def run(url):
    u_obj = common.URL(url)
    _u = u_obj.scheme + '://' + u_obj.netloc + u_obj.path + u_obj.filename
    if _u not in common.BACKUPDOWN_LIST:
        if os.path.splitext(_u)[1].lower() in INCLUDED_SUFFIX:
            task = []
            task.append(threading.Thread(target=VimDown(_u).download, args=()))
            task.append(threading.Thread(target=GeditDown(_u).download, args=()))

            for _ in task:
                _.start()
            for _ in task:
                _.join()
    print 'END'
