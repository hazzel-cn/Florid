import lib.common

MODULE_NAME = str(__file__).split('/')[-1].split('\\')[-1].replace('.pyc', '').replace('.py', '')


def init():
    pass


def run(url_obj):
    import time
    time.sleep(1)
    if url_obj.value.count('1') >= 6:
        lib.common.RESULT_DIRECROTY[MODULE_NAME].append(url_obj.value)
    lib.common.CHECKED_COUNT[MODULE_NAME] += 1
    lib.common.ALL_DOWN_COUNT += 1

