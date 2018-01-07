import lib.common

MODULE_NAME = 'sample-1'


def run():
    lib.common.RESULT_ONE_DICT['IP Info'] = 'http://toolbar.netcraft.com/site_report?url=%s' % lib.common.SOURCE_URL
    lib.common.ALIVE_LINE[MODULE_NAME] += 1
