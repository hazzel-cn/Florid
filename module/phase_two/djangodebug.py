import lib.common
import lib.urlentity

MODULE_NAME = 'djangodebug'


def init():
    pass


def run(url):
    if 'Server' in lib.common.RESULT_ONE_DICT:
        server_info = lib.common.RESULT_ONE_DICT['Server'].lower()
        if 'wsgiserver' or 'python' in server_info:
            # print 'is python'
            url_obj = lib.urlentity.URLEntity(url)
            if url_obj.get_query() is not None:
                # print 'is not none query'
                new_url_obj = lib.urlentity.URLEntity(url_obj.get_url().replace('=', '=%bf'))
                # print new_url_obj.get_url()
                new_url_obj.make_get_request()
                # print new_url_obj.get_response().text[:10]
                res = new_url_obj.get_response().text.lower()
                # print 'html', res
                import time
                time.sleep(2)
                if 'exception' or 'debug = true' or 'traceback' in res:
                    lib.common.RESULT_DICT[MODULE_NAME].append(new_url_obj.get_url())
    lib.common.ALIVE_LINE[MODULE_NAME] += 1
