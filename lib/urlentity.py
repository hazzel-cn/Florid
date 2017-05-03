# coding=utf-8
# This file provide the class of URL which contains elements of an URL
import re


class URLEntity(object):
    # The class of standard url. It contains the elements of a parsed url
    def __init__(self, raw_url):
        raw_url = raw_url if re.match('^\w+://', raw_url) else 'http://'+raw_url
        cut_url = re.findall('(^[^\?]+)\??(.*)', raw_url)
        body = cut_url[0][0]

        self.query = cut_url[0][1]
        self.hostname = '' if not re.match('^[\w]+://.+', body) else re.findall('^\w+://([^/:]+):?.*', body)[0]
        self.scheme = re.findall('^(\w+)://.*$', body)[0]
        self.port = '80' if not re.match('^\w+://[^:]+:\d+', body) else re.findall('^\w+://[^:]+:(\d+)', body)[0]
        # print self.port

        self.body = body if not body.endswith(self.hostname) and not body.endswith(self.port) else body + '/'
        self.value = raw_url if not raw_url.endswith(self.hostname) and not raw_url.endswith(self.port) else raw_url + '/'
        self.path = '/' if not re.match('\w.+://[^/]+/.*/[^/]*$', self.body) else re.findall('\w.+://[^/]+(/.*/)[^/]*$', self.body)[0]

        self.type = 'D' if self.value.endswith('/') else 'F'
        self.filename = '' if self.type == 'D' else re.findall('^.*/([^/]+)', self.body)[0]
        self.dir = re.findall('(.+/).*', self.body)[0]
        # print re.findall('([\w]+://[^/]+/).*', self.body), self.dir
        self.source = '/' if self.dir == 'http://' else re.findall('([\w]+://[^/]+/).*', self.body)[0]

    def __str__(self):
        return self.value


if __name__ == '__main__':
    from pprint import pprint
    url = []
    url.append('ftp://www.floridhazel.com:9999/admin/manage/index.php?id=1&p=admin')
    url.append('www.floridhazel.com:9999/admin/manage/index.php?id=1&p=admin')
    url.append('ftp://www.floridhazel.com:9999/admin/manage/index.php')
    url.append('ftp://www.floridhazel.com:9999/admin/manage/')
    url.append('ftp://www.floridhazel.com:9999/admin/')
    url.append('ftp://www.floridhazel.com:9999/')
    url.append('ftp://www.floridhazel.com:9999')

    url.append('ftp://www.floridhazel.com/admin/manage/index.php?id=1&p=admin')
    url.append('www.floridhazel.com/admin/manage/index.php?id=1&p=admin')
    url.append('ftp://www.floridhazel.com/admin/manage/index.php')
    url.append('ftp://www.floridhazel.com/admin/manage/')
    url.append('ftp://www.floridhazel.com/admin/')
    url.append('ftp://www.floridhazel.com/')
    url.append('ftp://www.floridhazel.com')

    for u in url:
        url_obj = URLEntity(raw_url=u)
        print '\n', url_obj
        pprint(url_obj.__dict__)
