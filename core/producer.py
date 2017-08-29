import os
import urlparse

import requests
import bs4

import lib.common
import lib.urlentity
import lib.colorprint


class Producer(object):
    def __init__(self, source_url):
        self.__source_url_obj = lib.urlentity.URLEntity(source_url)

        self.waiting_list = [self.__source_url_obj.get_url()]
        self.crawled_list = [self.__source_url_obj.get_url()]

        # Create the directory for log files such as the list of urls
        if not os.path.exists(lib.common.CONFIG['project_path'] + '/log/' + self.__source_url_obj.get_hostname()):
            try:
                os.makedirs(lib.common.CONFIG['project_path'] + '/log/' + self.__source_url_obj.get_hostname())
            except Exception, e:
                print 'Creating Log File Fail.'
        self.log_fp = open(
            lib.common.CONFIG['project_path'] + '/log/' + self.__source_url_obj.get_hostname() + '/urllist.txt', 'w+')

    def __find_joint(self, soup, tag1, tag2):
        for tag in soup.find_all(tag1):
            url_new = urlparse.urljoin(self.__source_url_obj.get_url(), tag.get(tag2))
            url_new_obj = lib.urlentity.URLEntity(url_new)
            if url_new_obj.get_url() not in self.crawled_list and url_new_obj.get_hostname() == self.__source_url_obj.get_hostname() and '#' not in url_new_obj.get_url():
                self.waiting_list.append(url_new_obj.get_url())
                self.crawled_list.append(url_new_obj.get_url())

    def run(self):
        lib.colorprint.color().blue('[*] Scanning')
        while not lib.common.FLAG['producer_done']:
            while len(self.waiting_list) > 0:
                print '\r+ ' + self.waiting_list[0]
                try:
                    r = requests.get(url=self.waiting_list[0])
                    soup = bs4.BeautifulSoup(r.text, 'html.parser')
                except Exception, e:
                    self.waiting_list.pop(0)
                    continue

                lib.common.CHECKER_OBJ.queue_add(url=self.waiting_list[0])
                self.log_fp.writelines(self.waiting_list[0] + '\n')
                self.waiting_list.pop(0)

                self.__find_joint(soup=soup, tag1='a', tag2='href')
                self.__find_joint(soup=soup, tag1='form', tag2='action')
                self.__find_joint(soup=soup, tag1='link', tag2='href')
            lib.common.FLAG['producer_done'] = True
        lib.colorprint.color().yellow('[*] ' + str(lib.common.CHECKER_OBJ.get_total_length()) + ' URLs Found', end='\n\n')


if __name__ == '__main__':
    producer = Producer('http://testphp.vulnweb.com/').run()
