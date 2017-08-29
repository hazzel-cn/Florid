import pprint
import lib.common
import lib.colorprint


class Checker(object):
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
        while len(self.all_module_list) != 0:
            if lib.common.FLAG['producer_done']:
                # print the result of phase one
                if not self.phase_one_printed and len(lib.common.RESULT_ONE_DICT) == len(lib.common.MODULE_ONE_NAME_LIST):
                    lib.colorprint.color().sky_blue('[=== Site Info ===]')
                    for __key in lib.common.RESULT_ONE_DICT:
                        print __key + ':\t' + lib.common.RESULT_ONE_DICT[__key]
                    self.phase_one_printed = True
                    print

                for __module_name in self.all_module_list:
                    if lib.common.ALIVE_LINE[__module_name] >= 0:
                        lib.colorprint.color().sky_blue('[=== ' + __module_name + ' ===]')
                        self.all_module_list.remove(__module_name)
                        pprint.pprint(lib.common.RESULT_DICT[__module_name])
        lib.common.FLAG['scan_done'] = True
