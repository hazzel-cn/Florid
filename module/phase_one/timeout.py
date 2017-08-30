import time

import lib.common
import lib.urlentity

MODULE_NAME = 'timeout'


def run():
    time_list = list([])
    old_time = time.time()

    url_obj = lib.urlentity.URLEntity(lib.common.SOURCE_URL)
    for i in range(0, 4):
        url_obj.make_get_request()
        time_list.append(time.time() - old_time)
        old_time = time.time()
    lib.common.TIME_OUT = max(reduce(lambda x, y: x + y, time_list) / 4, 5)
    lib.common.ALIVE_LINE[MODULE_NAME] += 1
