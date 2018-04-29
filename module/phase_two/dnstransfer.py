import os
import re
import threading

import lib.common
import lib.urlentity

MODULE_NAME = 'dnstransfer'

global dns_transfer_is_vul


def init():
    global dns_transfer_is_vul
    dns_transfer_is_vul = False


def transfer_try(domain, dns):
    global dns_transfer_is_vul
    subdomain = os.popen("dig @%s %s axfr" % (dns, domain)).read()
    if subdomain.find('Transfer failed') == -1 and subdomain.find('timed out') == -1 and subdomain.find(
            'not found') == -1 and subdomain.find('XFR size') > 0:
        dns_transfer_is_vul = True


def dns_retrieve(domain):
    dig = os.popen("dig ns %s" % domain).read()
    dns_list = re.findall(r'NS\t(.*?).\n', dig)
    return dns_list


def domain_retrieve(url):
    url_obj = lib.urlentity.URLEntity(url)
    domains = '.'.join(url_obj.get_hostname().split('.')[1:])
    return domains


def run(url):
    global dns_transfer_is_vul
    domain = domain_retrieve(url=lib.common.SOURCE_URL)
    dns_list = dns_retrieve(domain=domain)
    tasks = []
    for dns in dns_list:
        t = threading.Thread(target=transfer_try, args=(domain, dns))
        tasks.append(t)
        t.setDaemon(True)
        t.start()
    for _t in tasks:
        _t.join()

    if dns_transfer_is_vul:
        lib.common.RESULT_DICT[MODULE_NAME].append('Potential DNS Transfer Vulnerability Detected!')
    lib.common.ALIVE_LINE[MODULE_NAME] += 1


if __name__ == '__main__':
    print domain_retrieve('http://www.whu.edu.cn/')
