#!/usr/bin/python
# -*-coding:utf-8-*-
import requests
import time
import json
import time


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
            print '[*] Task Completed: %s' % self.taskid
            return True
        return False

    def __statuscheck(self):
        return json.loads(requests.get(self.sqlmapurl + '/scan/' + self.taskid + '/status').text)['status']

    def __resultcheck(self):
        self.result = json.loads(requests.get(self.sqlmapurl + '/scan/' + self.taskid + '/data').text)['data']
        if len(self.result) > 0:
            print '\033[32m[*] The Page is Vul\033[0m'
            self.resultvalue = self.result[1]['value'][0]
            print '  \033[32m\33[1m' + self.resultvalue['dbms'], self.resultvalue['dbms_version'][0], self.resultvalue['place'] + '\033[0m'
            for i in range(0, 10):
                try:
                    print '    [payload]:\t\033[32m%s\033[0m' % self.resultvalue['data'][str(i)]['payload']
                except:
                    pass
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
            r = requests.post(url = self.sqlmapurl + '/scan/' + self.taskid + '/start', data = json.dumps(self.data), headers = self.headers)
        while self.__statuscheck() != 'terminated':
            time.sleep(1)
        self.__resultcheck()
        return True


    def run(self):
        if self.__newtask():
            if self.__starttask():
                self.__deletetask()


def init():
    try:
        r = requests.get(SQLMAP_URL)
        return True
    except Exception as e:
        if type(e) == requests.exceptions.ConnectionError:
            return 'Please run the "sqlmapapi.py" first'


def run(options):
    a = SqlInjectionCheck(SQLMAP_URL, options.url)
    a.run()