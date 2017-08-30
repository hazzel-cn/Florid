import re
import time

import requests

import lib.common


class URLEntity:
    def __init__(self, raw_url):
        self.__url = raw_url
        self.__scheme = str()
        self.__host = str()
        self.__port = int()
        self.__path = str()
        self.__file = str()
        self.__source = str()
        self.__query = str()
        self.__isFile = bool()
        self.__response = None

        # To match scheme
        try:
            self.__scheme = re.findall('^([a-zA-Z]*)://', self.__url)[0]
        except IndexError, SchemeNotFound:
            self.__scheme = 'http'
            self.__url = self.__scheme + '://' + self.__url

        # To match host
        try:
            self.__host = re.findall('^[a-zA-Z]+://([^/:]+)', self.__url)[0]
        except IndexError, HostnameNotFound:
            self.__host = ''
            print HostnameNotFound

        # To match port
        try:
            self.__port = int(re.findall('^[a-zA-Z]+://[^:]+:([0-9]+)/', self.__url)[0])
        except IndexError, PortNotFound:
            self.__port = 80

        # To format the url
        if re.match('[a-zA-Z]+://[^/]+$', self.__url):
            self.__url += '/'

        # To match file
        try:
            self.__file = re.findall('^[a-zA-Z]+://[^?]*/([^/?]*)?', self.__url)[0]
        except IndexError, FileNotFound:
            self.__file = ''

        # To match source
        try:
            self.__source = re.findall('^([a-zA-Z]+://[^/]+/)', self.__url)[0]
        except IndexError, SourceNotFound:
            self.__source = re.findall('^([a-zA-Z]+://[^:/]+)/', self.__url)[0]

        # To match path
        try:
            self.__path = re.findall('^[a-zA-Z]+://[^/]+([^?]*)', self.__url)[0]
            self.__path = self.__path.replace(self.__file, '')
        except IndexError, PathNotFound:
            self.__path = '/'

        # To match query
        try:
            self.__query = re.findall('\?(.+)', self.__url)[0]
        except IndexError, QueryNotFound:
            self.__query = ''

        # To match url type
        self.__isFile = True if self.__file != '' else False

    def __str__(self):
        return self.__url

    def get_url(self):
        return self.__url

    def get_scheme(self):
        return self.__scheme

    def get_hostname(self):
        return self.__host

    def get_port(self):
        return self.__port

    def get_file(self):
        return self.__file

    def get_source(self):
        return self.__source

    def get_path(self):
        return self.__path

    def get_query(self):
        return self.__query

    def is_file(self):
        return self.__isFile

    def make_get_request(self, timeout=lib.common.TIME_OUT, delay=0):
        try:
            time.sleep(delay)
            self.__response = requests.get(self.__url, timeout=timeout)
        except Exception:
            self.__response = None

    def make_post_request(self, data, timeout=lib.common.TIME_OUT, delay=0):
        try:
            time.sleep(delay)
            self.__response = requests.post(self.__url, data=data, timeout=timeout)
        except Exception:
            self.__response = None

    def get_response(self):
        return self.__response


# Only for test below
if __name__ == '__main__':
    test_case = list()
    # test_case.append('ftp://www.floridhazel.com:9999/admin/manage/index.php?id=1&p=admin')
    # test_case.append('www.floridhazel.com:9999/admin/manage/index.php?id=1&p=admin')
    # test_case.append('ftp://www.floridhazel.com:9999/admin/manage/index.php')
    # test_case.append('ftp://www.floridhazel.com:9999/admin/manage/')
    # test_case.append('ftp://www.floridhazel.com:9999/admin/')
    # test_case.append('ftp://www.floridhazel.com:9999/')
    # test_case.append('ftp://www.floridhazel.com:9999')

    test_case.append('http://www.floridhazel.com:900/admin/manage/index.php?id=1&p=./admin.jpg')
    test_case.append('www.floridhazel.com/admin/manage/index.php?id=1&p=admin')
    test_case.append('http://www.floridhazel.com/admin/manage/index.php')
    test_case.append('http://www.floridhazel.com/admin/manage/')
    test_case.append('http://www.floridhazel.com/admin/')
    test_case.append('http://www.floridhazel.com/')
    test_case.append('http://www.floridhazel.com')
    test_case.append('floridhazel.com')
    for url in test_case:
        url_entity = URLEntity(raw_url=url)
        print url
        import pprint

        # url_entity.make_get_request()
        pprint.pprint(url_entity.__dict__)
        print
