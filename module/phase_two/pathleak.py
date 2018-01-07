import lib.common
import lib.urlentity

MODULE_NAME = 'pathleak'


def init():
    pass


def run(url):
    url_obj = lib.urlentity.URLEntity(raw_url=url)

    if url_obj.is_file():
        if url_obj.get_query() != '':
            query_list = url_obj.get_query().split('&')
            for item_num in range(len(query_list)):
                tmp_query_list = list(query_list)
                tmp_query_list[item_num].replace(tmp_query_list[item_num].split('=')[-1], '')
                tmp_url = url_obj.get_source() + url_obj.get_file() + '?' + ''.join(tmp_query_list)
                tmp_url_obj = lib.urlentity.URLEntity(raw_url=tmp_url)
                tmp_url_obj.make_get_request()
                html_text = tmp_url_obj.get_response().text.lower()
                if 'directory listing' in html_text.lower():
                    lib.common.RESULT_DICT[MODULE_NAME].append(tmp_url)

    if not url_obj.is_file():
        if 'directory listing' in url_obj.get_response().text.lower():
            lib.common.RESULT_DICT[MODULE_NAME].append(tmp_url)

    lib.common.ALIVE_LINE[MODULE_NAME] += 1
