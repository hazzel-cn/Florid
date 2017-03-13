#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urlparse

import requests
from bs4 import BeautifulSoup

import lib.common as common

MODULE_NAME = 'spider'
SESITIVE_SUFFIX = ['.zip']


class Spider(object):
    def __init__(self, source_url):
        self.source_url = source_url
        self.url_object = urlparse.urlparse(self.source_url)
        self.netloc = self.url_object.netloc
        self.hostname = self.url_object.hostname
        self.url_list = [self.source_url]
        self.visited_list = [self.source_url]

        if not os.path.exists('log/' + self.netloc + '/'):
            os.makedirs('log/' + self.netloc + '/')
        self.txt = open('log/' + self.netloc + '/url_list.txt', 'w+')

    def save_locker(self):
        while common.SPIDER_END and common.TASK_QUEUE.qsize() > 0:
            if common.LOCKER.acquire():
                common.LOCKER.notifyAll()
                common.LOCKER.release()

    def crawl(self):
        # print 'begin to crawl'
        while len(self.url_list) > 0:
            if os.path.splitext(os.path.basename(self.url_list[0]))[1] in SESITIVE_SUFFIX:
                common.SENSITIVE_LIST.append(self.url_list[0])
                self.url_list.pop(0)

            try:
                r = requests.get(self.url_list[0])
            except:
                print 'fail'
                common.SENSITIVE_LIST.append(self.url_list[0])
                self.url_list.pop(0)
                continue

            if r.status_code != 404:
                html_text = r.text
            self.txt.writelines(self.url_list[0].encode('utf-8') + '\n')
            self.soup = BeautifulSoup(html_text, 'html.parser')

            self.current_url = self.url_list[0]

            for tag in self.soup.findAll('form', action=True):
                url_new = urlparse.urljoin(self.current_url, tag['action'])
                if self.netloc.split('.')[-2] in urlparse.urlparse(
                        url_new).netloc and url_new not in self.visited_list and '#' not in url_new:
                    self.url_list.append(url_new)
                    self.visited_list.append(url_new)
            for tag in self.soup.findAll('a', href=True):
                url_new = urlparse.urljoin(self.current_url, tag['href'])
                if self.netloc.split('.')[-2] in urlparse.urlparse(
                        url_new).netloc and url_new not in self.visited_list and '#' not in url_new:
                    self.url_list.append(url_new)
                    self.visited_list.append(url_new)
            # print 'Spider getting locker'
            if common.LOCKER.acquire():
                common.TASK_QUEUE.put(self.current_url)
                common.LOCKER.notify()
                common.LOCKER.release()
            self.url_list.pop(0)

        common.SPIDER_END = True
        # threading.Thread(target=self.save_locker, args=()).start()
        return True


def init():
    return (True, 'SUCCESS')


def run():
    print '[*] Running....'
    a = Spider(common.WebInfo.url).crawl()
    # print '[*] Complete'
