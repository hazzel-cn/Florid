#!/usr/bin/python
# -*-coding:utf-8-*-
import os
import requests
import urlparse
import time
import json
import time
import threading


MODULE_NAME = 'sqli'
SQLMAP_URL = 'http://127.0.0.1:8775'


class SqlInjectionCheck(object):

    def __init__(self, sqlmapurl, targeturl):
        self.sqlmapurl = sqlmapurl
        self.targeturl = targeturl

    def __newtask(self):
        self.taskid = requests.get(self.sqlmapurl + '/task/new').json()['taskid']
        #print '[*] New Task ID: %s' % self.taskid
        if len(self.taskid) > 0:
            return True
        return False


    def __deletetask(self):
        if json.loads(requests.get(self.sqlmapurl + '/task/' + self.taskid + '/delete').text)['success']:
            #print '[*] Task Completed: %s' % self.taskid
            return True
        return False

    def __statuscheck(self):
        return json.loads(requests.get(self.sqlmapurl + '/scan/' + self.taskid + '/status').text)['status']

    def __resultcheck(self):
        self.result = json.loads(requests.get(self.sqlmapurl + '/scan/' + self.taskid + '/data').text)['data']
        if len(self.result) > 0:
            print '\033[32m[*] The Page is Vul\033[0m: %s' % self.targeturl
            self.resultvalue = self.result[0]['value'][0]
            try:
                print '  \033[32m\33[1m' + self.resultvalue['dbms'], self.resultvalue['place'] + '\033[0m'
            except:
                pass
            for i in range(0, 10):
                try:
                    print '    [payload]:\t\033[32m%s\033[0m' % self.resultvalue['data'][str(i)]['payload']
                except:
                    pass
            return True
        else:
            #print '[*] The page is not Vul'
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
        if self.__resultcheck():
            return True
        else:
            return False


    def run(self):
        if self.__newtask():
            if self.__starttask():
                return True
            else:
                return False
            self.__deletetask()


def init():
    try:
        r = requests.get(SQLMAP_URL)
        return True
    except Exception as e:
        if type(e) == requests.exceptions.ConnectionError:
            return 'Please run the "sqlmapapi.py" first'
        else:
            return 'Unknown Error'


def run(options):
    VERBOSE = options.verbose

    urls = []
    urls_p = []
    urls_s = []
    for _line in open('log/'+options.hostname+'/url_list.txt'):
        _url = _line.replace('\n', '')
        if urlparse.urlparse(_url).query != '':
            if os.path.basename(_url).replace(urlparse.urlparse(_url).query, '').replace('?','') not in urls_p:
                if VERBOSE:
                    print _url
                urls.append(_url)
                urls_p.append(os.path.basename(_url).replace(urlparse.urlparse(_url).query, '').replace('?',''))
    print '[*] URL List Loaded.'

    threads = []
    print '[*] ', len(urls), 'Cases to test...'
    for _u in urls:
        a = SqlInjectionCheck(SQLMAP_URL, _u)
        threads.append(threading.Thread(target=a.run,args=()))
    for t in threads:
        t.setDaemon(True)
        t.start()
        time.sleep(10)
    while threading.activeCount() > 0:
        print threading.activeCount(), '\rActive Threads Number:',
        time.sleep(1)
