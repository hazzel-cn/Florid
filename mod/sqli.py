#!/usr/bin/python
# -*-coding:utf-8-*-
import requests
import json


MODULE_NAME = 'sqli'
SQLMAP_URL = 'http://127.0.0.1:8775'


class SqlInjectionCheck(object):

    def __init__(self, sqlmapurl, targeturl):
        self.sqlmapurl = sqlmapurl
        self.targeturl = targeturl

    def __newtask(self):
        self.taskid = requests.get(self.sqlmapurl + '/task/new').json()['taskid']
        print '[*] Task ID: %s' % self.taskid
        if len(self.taskid) > 0:
            return True
        return False

    def __deletetask(self):
        if json.loads(requests.get(self.sqlmapurl + '/task/' + self.taskid + '/delete').text)['success']:
            print '[*] Task Deleted: %s' % self.taskid
            return True
        return False

    def __statuscheck(self):
        return json.loads(requests.get(self.sqlmapurl + '/scan/' + self.taskid + '/status').text)['status']

    def __resultcheck(self):
        self.result = json.loads(requests.get(self.sqlmapurl + '/scan/' + self.taskid + '/data').text)['data']
        if len(self.result) > 0:
            print '[*] The Page is Vul: %s' % self.result
            return True
        else:
            print '[*] The page is not Vul'
            return False

    def __starttask(self):
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.data = {
            'url': self.targeturl
        }
        while self.__statuscheck() == 'not running':
            print 'Scanning...',
            r = requests.post(url = self.sqlmapurl + '/scan/' + self.taskid + '/start', data = json.dumps(self.data), headers = self.headers)
            print requests.get(self.sqlmapurl + '/scan/' + self.taskid + '/data').json()
            if len(str(r.json()['engineid'])) > 0:
                print r.json()['engineid']
        self.__resultcheck()
        return True


    def run(self):
        if self.__newtask():
            if self.__starttask():
                self.__deletetask()


def run(options):
    a = SqlInjectionCheck(SQLMAP_URL, options.url)
    a.run()