import os
import urlparse

import bs4
import requests

import lib.colorprint
import lib.common
import lib.urlentity


class Spider(object):
    def __init__(self, raw_url):
        self.raw_url_obj = lib.urlentity.URLEntity(raw_url)
        self.value = self.raw_url_obj.value
        self.hostname = self.raw_url_obj.hostname
        self.__create_log_direcroty()
        self.fp_log = open(lib.common.PROJECT_PATH + '/log/' + self.hostname + '/urllist.txt', 'w+')

    def __create_log_direcroty(self):
        if not os.path.exists(lib.common.PROJECT_PATH + '/log/' + self.hostname):
            os.makedirs(lib.common.PROJECT_PATH + '/log/' + self.hostname)

    def __save_queue(self, url):
        lib.common.URL_QUEUE.put(lib.urlentity.URLEntity(url))
        lib.common.URL_COUNT += 1
        lib.common.CURRENT_URL = url
        lib.colorprint.color().yellow('\r + %s\n' % url)
        self.fp_log.writelines(url+'\n')

    def run(self):
        lib.colorprint.color().sky_blue('>>>>>> [Site Map]\n')
        waiting_list = [self.value]
        crawled_list = [self.value]

        while len(waiting_list) > 0:
            try:
                r = requests.get(url=waiting_list[0])
                soup = bs4.BeautifulSoup(r.text, 'html.parser')
            except Exception, e:
                # print '[Warning] Connection Bad', e
                waiting_list.pop(0)
                continue

            self.__save_queue(waiting_list[0])
            waiting_list.pop(0)

            for tag in soup.find_all('a'):
                url_new = urlparse.urljoin(self.value, tag.get('href'))
                url_new_obj = lib.urlentity.URLEntity(url_new)
                if url_new_obj.value not in crawled_list \
                        and url_new_obj.hostname == self.hostname \
                        and '#' not in url_new_obj.value:
                    waiting_list.append(url_new_obj.value)
                    crawled_list.append(url_new_obj.value)
                    # print url_new
            for tag in soup.find_all('form'):
                url_new = urlparse.urljoin(self.value, tag.get('action'))
                url_new_obj = lib.urlentity.URLEntity(url_new)
                if url_new_obj.value not in crawled_list \
                        and url_new_obj.hostname == self.hostname \
                        and '#' not in url_new:
                    waiting_list.append(url_new_obj.value)
                    crawled_list.append(url_new_obj.value)

        lib.colorprint.color().blue('=' * 40 + '\n')
        # lib.colorprint.color().blue(' ' * 10 + '*' * 20 + ' ' * 10 + '\n')
        lib.colorprint.color().blue('=' * 40 + '\n')

        lib.colorprint.color().green('[Site Info]' + '\n')
        for _m_name in lib.common.MODULE_NAME_SET_PRE:
            lib.colorprint.color().green(' + ' + lib.common.RESULT_DIRECROTY[_m_name][0] + '\n')
            # print len(lib.common.RESULT_DIRECROTY[_m_name]), type(lib.common.RESULT_DIRECROTY[_m_name])
        lib.common.SPIDER_DONE_FLAG = True

        # pprint.pprint(waiting_list)


if __name__ == '__main__':
    spider = Spider('http://www.floridhazel.com')
