import Queue
import platform
import threading
import urlparse

import requests

# Global Variety

LOCKER = threading.Condition()
SPIDER_END = False
TASK_QUEUE = Queue.Queue()
requests.keep_alive = False

PLATFORM_WIN = True
# True for Win
# False for Linux or MacOS


SENSITIVE_LIST = []
BACKUPDOWN_LIST = []

LOG_FILE = ''
LOG_DICT = ''


class WebInfo(object):
    modules = []
    modules_list = {}
    url = ''
    os = platform.system()

    def __init__(self):
        pass


class URL(object):
    def __init__(self, url):

        if url.endswith(urlparse.urlparse(url).netloc):
            self.value = url + '/'
        else:
            self.value = url
        if not url.startswith('http'):
            self.value = 'http://' + self.value

        parsed_url = urlparse.urlparse(self.value)

        path_list = parsed_url.path.split('/')
        query_list = parsed_url.query.split('&')
        while '' in path_list:
            path_list.remove('')

        self.scheme = parsed_url.scheme
        self.netloc = parsed_url.netloc
        self.file = parsed_url.path.split('/')

        if self.value.endswith('/'):
            self.type = 'D'
            self.filename = ''
        else:
            self.type = 'F'
            self.filename = path_list[-1]

        self.path = parsed_url.path.replace(self.filename, '')
        self.query = {}
        if query_list != ['']:
            for _ in query_list:
                self.query[_.split('=')[0]] = _.split('=')[1]
        return None
