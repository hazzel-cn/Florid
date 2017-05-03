# coding=utf-8
import lib.common
import pprint
import lib.colorprint


def run():
    show_result_set = []
    # do not stop until all result has been showed
    while len(show_result_set) != len(lib.common.MODULE_DIRECTORY):
        for __module_pointer in lib.common.CHECKED_COUNT:
            # Once the module checked all urls: show result
            if lib.common.SPIDER_DONE_FLAG \
                    and lib.common.CHECKED_COUNT[__module_pointer] == lib.common.URL_COUNT \
                    and __module_pointer not in show_result_set:
                lib.colorprint.color().sky_blue(' ' * 30 + '\n>>>>>> [%s]\n' % __module_pointer)
                pprint.pprint(lib.common.RESULT_DIRECROTY[__module_pointer])
                show_result_set.append(__module_pointer)
