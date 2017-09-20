import threading

import config
import lib.common


class Consumer(object):
    def __int__(self):
        pass

    # While the spider is still working or the queue is not empty yet
    def run(self):
        for __module_name in lib.common.MODILE_ONE_OBJ_DICT:
            threading.Thread(target=lib.common.MODILE_ONE_OBJ_DICT[__module_name].run, args=()).start()
        while not lib.common.CHECKER_OBJ.get_producer_state() or lib.common.CHECKER_OBJ.get_queue_length() > 0:
            if config.config['exit_without_result']:
                if lib.common.FLAG['stop_signal']:
                    break
            if lib.common.CHECKER_OBJ.get_queue_length() > 0:
                url_to_be_checked = lib.common.CHECKER_OBJ.queue_pop()
                for __module_name in lib.common.MODULE_OBJ_DICT:
                    lib.common.ALIVE_LINE[__module_name] -= 1
                    t = threading.Thread(target=lib.common.MODULE_OBJ_DICT[__module_name].run,
                                         args=(url_to_be_checked,))
                    t.setDaemon(True)
                    t.start()
