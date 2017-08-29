import lib.common
import requests
import time
import hashlib

MODULE_NAME = 'sample-1'


def init():
    pass


def run():
    '''Fuck, I failed to fuck it out
    s = requests.Session()
    headers = {
        'Host': 'toolbar.netcraft.com',
        'User-Agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko / 20100101 Firefox / 55.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }
    s.get(url='http://toolbar.netcraft.com/site_report', headers=headers)
    print s.cookies
    challenge = s.cookies['netcraft_js_verification_challenge']
    res = hashlib.sha1(challenge).hexdigest()

    print challenge
    print res

    s.cookies['netcraft_js_verification_response'] = res
    time.sleep(0.5)

    cookies = {
        'netcraft_js_verification_challenge': challenge,
        'netcraft_js_verification_response': res
    }
    print s.cookies
    url_query = 'http://toolbar.netcraft.com/site_report?url=' + lib.common.SOURCE_URL
    r = s.get(url=url_query, headers=headers)

    print r.text
    '''

    lib.common.RESULT_ONE_DICT['IP Info'] = 'http://toolbar.netcraft.com/site_report?url=%s' % lib.common.SOURCE_URL
