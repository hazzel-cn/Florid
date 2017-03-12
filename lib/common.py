import Queue
import platform
import threading

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


class WebInfo(object):
    modules = []
    modules_list = {}
    url = ''
    os = platform.system()

    def __init__(self):
        pass
