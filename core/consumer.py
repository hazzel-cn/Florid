import threading

import config.config
import lib.common


class Consumer(object):
    # A class designed to call Checker to consume URLs in Checker queue.
    def __int__(self):
        pass

    def run(self):
        # Run all modules in phase one to check the source URL.
        # That's why there is no URL as parameter.
        for __module_name in lib.common.MODULE_ONE_OBJ_DICT:
            threading.Thread(target=lib.common.MODULE_ONE_OBJ_DICT[__module_name].run, args=()).start()

        # While the checker still needs to work, or
        # while printer still needs to work due to the items in the Checker queue.
        while not lib.common.CHECKER_OBJ.get_producer_state() or lib.common.CHECKER_OBJ.get_queue_length() > 0:
            # Break immediately? Due to the config.py
            if config.config.config['exit_without_result']:
                if lib.common.FLAG['stop_signal']:
                    break
            # If printer needs to work,
            # get one URL from the Checker queue,
            # hand this URL to all modules.
            if lib.common.CHECKER_OBJ.get_queue_length() > 0:
                url_to_be_checked = lib.common.CHECKER_OBJ.queue_pop()
                for __module_name in lib.common.MODULE_OBJ_DICT:
                    # Every time a URL is submitted to a module, the ALIVE_LINE of this module will minus one.
                    # Every time this module checked a URL, this value will be added by one.
                    # (This is implemented in each module)
                    lib.common.ALIVE_LINE[__module_name] -= 1
                    t = threading.Thread(target=lib.common.MODULE_OBJ_DICT[__module_name].run,
                                         args=(url_to_be_checked,))
                    t.setDaemon(True)
                    t.start()
