# coding=utf-8
# The file distribute the URL to modules
import lib.common
import threading
import lib.urlentity
import lib.colorprint


def distribute_url(url_obj):
    for __module_name in lib.common.MODULE_DIRECTORY:
        threading.Thread(target=lib.common.MODULE_DIRECTORY[__module_name].run, args=(url_obj,)).start()



def distribute_path(path_obj):
    print path_obj.value


def consume():
    while not lib.common.SPIDER_DONE_FLAG:
        if lib.common.URL_QUEUE.qsize() > 0:
            threading.Thread(target=distribute_url, args=(lib.common.URL_QUEUE.get(),)).start()
        if lib.common.PATH_QUEUE.qsize() > 0:
            threading.Thread(target=distribute_path, args=(lib.common.PATH_QUEUE.get(),)).start()
