#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import urlparse

import requests

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
                return True
            else:
                pass
        except:
            pass
        return False


def init():
    return (True, 'SUCCESS')


def run(url):
    '''
    Plan to add the function which can add suffix automatically. e.g: when input www.hazzel.cn, it should be rewritten to www.hazzel.cn/index.php
    '''

    url = url.replace(urlparse.urlparse(url).query, '').replace('?', '')
    if urlparse.urlparse(url).path.endswith('/'):
        url = url + 'index.php'
    if os.path.splitext(os.path.basename(url))[1] in INCLUDED_SUFFIX:
        if VimDown(url).download() or GeditDown(url).download():
            print 'Success'
        else:
            print 'Fail'
    else:
        print 'Not Fail'
