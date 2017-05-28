# coding=utf-8
import pprint

import lib.colorprint
import lib.common


def run():
    show_result_set = []
    # do not stop until all result has been showed

    while len(show_result_set) != len(lib.common.MODULE_DIRECTORY):
        for __module_pointer in lib.common.CHECKED_COUNT:
            # Once the module checked all urls: show result
            # If spider is finished AND this module has checked all urls AND the result of the module has not been shown
            if lib.common.SPIDER_DONE_FLAG \
                    and lib.common.CHECKED_COUNT[__module_pointer] == lib.common.URL_COUNT \
                    and __module_pointer not in show_result_set:
                lib.colorprint.color().sky_blue(' ' * 30 + '\n>>>>>> [%s]\n' % __module_pointer)
                if len(lib.common.RESULT_DIRECROTY[__module_pointer]) != 0:
                    pprint.pprint(lib.common.RESULT_DIRECROTY[__module_pointer][0])
                show_result_set.append(__module_pointer)
