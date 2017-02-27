#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
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
        self.basename = os.path.basename(self.check_url).replace(urlparse.urlparse(self.check_url).query, '').replace('?','')

    def download(self):

        global VERBOSE

        for _ in SUFFIX_ARRAY:
            url_down = self.dirname + '/.' + self.basename + _

            try:
                r = requests.get(url_down, timeout=3)
                if r.status_code == 200:
                    print 'url_down\t[SUCCESS] <=============='
                    _f = open('log/'+self.hostname+'/'+self.basename+_, 'wb')
                    _f.write(r.content)
                else:
                    if VERBOSE:
                        print '  ', url_down, '\tFAIL'
            except:
                if VERBOSE:
                    print '  ', url_down, '\tFAIL'
        return True

class GeditDown(object):
    def __init__(self, check_url):
        self.check_url = check_url
        self.ob = urlparse.urlparse(self.check_url)
        self.scheme = self.ob.scheme
        self.hostname = self.ob.hostname
        self.dirname = os.path.dirname(self.check_url)
        self.basename = os.path.basename(self.check_url).replace(urlparse.urlparse(self.check_url).query, '').replace('?','')

    def download(self):
        url_down = self.check_url + '~'
        try:
            r = requests.get(url_down)
            if r.status_code == 200:
                print 'url_down\t[SUCCESS] <=============='
                _f = open('log/' + self.hostname + '/' + self.basename + '~', 'wb')
                _f.write(r.content)
            else:
                if VERBOSE:
                    print '  ', url_down, '\tFAIL'
        except:
            if VERBOSE:
                print '  ', url_down, '\tFAIL'
        return True


def init():
    return True

def run(options):
    global VERBOSE
    VERBOSE = options.verbose

    urls = []
    for _line in open('log/'+options.hostname+'/url_list.txt'):
        _url = _line.replace[:-1]
        _url = _url.replace(urlparse.urlparse(_url).query, '').replace('?','')
        if _url not in urls and os.path.splitext(os.path.basename(_url))[1] in INCLUDED_SUFFIX:
            urls.append(_url)
    print '[*] URL List Loaded.'
    print '[*] Scanning.....'

    for _u in urls:
        a = VimDown(_u).download()
        b = GeditDown(_u).download()
        time.sleep(0.5)
    print '[*] Finished'