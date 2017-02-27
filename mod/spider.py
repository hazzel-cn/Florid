import os
import requests
import urlparse
from bs4 import BeautifulSoup

MODULE_NAME = 'spider'


class Spider(object):
    def __init__(self, source_url):
        self.source_url = source_url
        self.url_object = urlparse.urlparse(self.source_url)
        self.netloc = self.url_object.netloc
        self.hostname = self.url_object.hostname
        self.url_list = [self.source_url]
        self.visited_list = [self.source_url]

        if not os.path.exists('log/' + self.hostname + '/'):
            os.makedirs('log/' + self.hostname + '/')
        self.txt = open('log/' + self.hostname + '/url_list.txt', 'w+')

    def crawl(self):
        # req = requests.Session()
        # req.cookies['PHPSESSID'] = 'nfcl6csp2kenfh9asafmhce804'

        while len(self.url_list) > 0:
            r = requests.get(self.url_list[0])
            if r.status_code != 404:
                html_text = r.text
            self.txt.writelines(self.url_list[0] + '\n')
            self.soup = BeautifulSoup(html_text, 'html.parser')

            self.current_url = self.url_list[0]
            self.obtmp = urlparse.urlparse(self.url_list[0])
            self.current_url_dirname = os.path.dirname(self.current_url)
            self.current_url_basename = os.path.basename(self.current_url)

            if VERBOSE:
                print '  ', self.url_list[0]
            self.url_list.pop(0)

            for tag in self.soup.findAll('form', action=True):
                url_new = urlparse.urljoin(self.current_url, tag['action'])
                if self.netloc in url_new and url_new not in self.visited_list and '#' not in url_new:
                    self.url_list.append(url_new)
                    self.visited_list.append(url_new)
            for tag in self.soup.findAll('a', href=True):
                url_new = urlparse.urljoin(self.current_url, tag['href'])
                if self.netloc in url_new and url_new not in self.visited_list and '#' not in url_new and 'logout' not in url_new:
                    self.url_list.append(url_new)
                    self.visited_list.append(url_new)

        return True


def init():
    return True


def run(options):
    global VERBOSE
    VERBOSE = options.verbose
    print '[*] Running....'
    a = Spider(options.url).crawl()
    print '[*] Complete'
