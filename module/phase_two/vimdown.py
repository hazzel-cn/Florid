import threading

import lib.common
import lib.urlentity

MODULE_NAME = 'vimdown'


def init():
    pass


def __download(url_obj, suffix):
    new_url = url_obj.get_url().replace(url_obj.get_file(), '.' + url_obj.get_file() + suffix)
    new_url_obj = lib.urlentity.URLEntity(new_url)
    new_url_obj.make_get_request()
    if new_url_obj.get_response() is not None:
        resp = new_url_obj.get_response()
        if resp.status_code != 404:
            lib.common.RESULT_DICT[MODULE_NAME].append(new_url)
            try:
                __file = open('log/' + url_obj.get_hostname() + '/' + url_obj.get_file() + suffix, 'w')
                __file.writelines(resp.content)
            except Exception, e:
                print 'Fail to download backup file', e
                pass  # Fail to write files.


def run(url):
    suffix_list = ['.swp', '.swn', '.swo', '.swp4']

    url_obj = lib.urlentity.URLEntity(raw_url=url)
    url_obj = lib.urlentity.URLEntity(raw_url=url_obj.get_url().replace('?' + url_obj.get_query(), ''))
    tasks = list([])
    if url_obj.is_file():
        for __suffix in suffix_list:
            t = threading.Thread(target=__download, args=(url_obj, __suffix))
            t.setDaemon(True)
            t.start()
        for t in tasks:
            t.join()
    lib.common.ALIVE_LINE[MODULE_NAME] += 1
