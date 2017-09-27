import lib.common
import lib.urlentity

MODULE_NAME = 'djangodebug'


def init():
    pass


def run(url):
    server_info = lib.common.RESULT_ONE_DICT['Server'].lower()
    if 'wsgiserver' or 'python' in server_info:
        url_obj = lib.urlentity.URLEntity(url)
        if url_obj.get_query() is not None:
            new_url_obj = lib.urlentity.URLEntity(url_obj.get_url().replace('=', '=%bf'))
            new_url_obj.make_get_request()
            res = new_url_obj.get_response().text.lower()
            if 'debug = true' in res or 'Traceback' in res or 'UnicodeEncodeError' in res:
                lib.common.RESULT_DICT[MODULE_NAME].append(new_url_obj.get_url())
    lib.common.ALIVE_LINE[MODULE_NAME] += 1
