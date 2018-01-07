import threading

import lib.common
import lib.urlentity

MODULE_NAME = 'hgcheck'


def init():
    lib.common.PUBLIC_STORAGE[MODULE_NAME] = []


def check(url_obj):
    new_url_obj = lib.urlentity.URLEntity(url_obj.get_url() + '.hg/')
    new_url_obj.make_get_request()
    if new_url_obj.get_response().status_code != 404:
        lib.common.RESULT_DICT[MODULE_NAME].append(new_url_obj.get_url())


def run(url):
    url_obj = lib.urlentity.URLEntity(raw_url=url)
    target_url = url_obj.get_source() + '/'
    target_url_list = list([target_url])
    if not url_obj.is_file():
        path_section_list = filter(lambda x: x != '', url_obj.get_path().split('/'))
        for path_section in path_section_list:
            target_url += (path_section + '/')
            target_url_list.append(target_url)

    tasks = list([])
    for url_to_be_checked in target_url_list:
        if url_to_be_checked not in lib.common.PUBLIC_STORAGE[MODULE_NAME]:
            lib.common.PUBLIC_STORAGE[MODULE_NAME].append(url_to_be_checked)
            url_to_be_checked_obj = lib.urlentity.URLEntity(url_to_be_checked)
            tasks.append(threading.Thread(target=check, args=(url_to_be_checked_obj,)))
    for t in tasks:
        t.setDaemon(True)
        t.start()
    for t in tasks:
        t.join()

    lib.common.ALIVE_LINE[MODULE_NAME] += 1
