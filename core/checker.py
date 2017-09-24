import config.config
import lib.colorprint
import lib.common


class Checker(object):
    # It's just a object to handle the URLs.
    # It works as a queue handler.
    def __init__(self):
        self.url_queue = []
        self.count_elements = 0

    def queue_add(self, url):
        self.url_queue.append(url)
        self.count_elements += 1

    def queue_pop(self):
        url = self.url_queue[0]
        self.url_queue.pop(0)
        return url

    def get_producer_state(self):
        return lib.common.FLAG['producer_done']

    def get_queue_length(self):
        return len(self.url_queue)

    def get_total_length(self):
        return self.count_elements


class ResultPrinter(object):
    def __init__(self):
        self.all_module_list = lib.common.MODULE_NAME_LIST
        self.phase_one_printed = False

    def run(self):
        # Do checking while modules left to be executed.
        while len(self.all_module_list) != 0:

            # If it finds the signal of stop, just stop.
            # It's based on the configuration.
            if config.config.config['exit_without_result']:
                if lib.common.FLAG['stop_signal']:
                    break

            # Wait until the producer's task is finished.
            # Or it will begin to check when there is no result
            if lib.common.FLAG['producer_done']:
                # Print the result of modules in phase one if it's not printed.
                if not self.phase_one_printed:
                    one_finish_count = 0
                    for __module_name in lib.common.MODULE_ONE_NAME_LIST:
                        one_finish_count += lib.common.ALIVE_LINE[__module_name]
                        # If the module's task is completed, the ALIVE_LINE value would be one.
                        # Else, it would be zero.

                    if one_finish_count == len(lib.common.MODULE_ONE_NAME_LIST):
                        lib.colorprint.color().sky_blue('[====\t' + 'Site Info'.ljust(14) + '====]')

                        longest_key = 0
                        for __key in lib.common.RESULT_ONE_DICT:
                            longest_key = max(longest_key, len(__key))
                        for __key in lib.common.RESULT_ONE_DICT:
                            print (__key + ': ').ljust(longest_key + 2) + lib.common.RESULT_ONE_DICT[__key]
                        self.phase_one_printed = True
                        print

                # The printing process for modules in phase one is completed.
                # Now it's time to print the results for modules in phase two.
                if self.phase_one_printed:
                    for __module_name in self.all_module_list:
                        if lib.common.ALIVE_LINE[__module_name] >= 0:
                            title = '[====\t' + __module_name.ljust(14) + '====]'
                            lib.colorprint.color().sky_blue(title)
                            self.all_module_list.remove(__module_name)
                            # Result of the certain module has been printed.
                            # Remove this module from the list.

                            for item in lib.common.RESULT_DICT[__module_name]:
                                lib.colorprint.color().green('\t> ' + item)
                            print

        if lib.common.FLAG['stop_signal']:
            lib.colorprint.color().yellow('[!] User abort. Results may be not completed.')
        lib.common.FLAG['scan_done'] = True
