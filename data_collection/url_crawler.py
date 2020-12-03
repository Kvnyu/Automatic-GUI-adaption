#coding = utf-8
import requests
from bs4 import BeautifulSoup
import re
import urllib.request

url = 'http://down.znds.com/applist-92-view.html?tid=92&TotalResult=45&orderby=view&PageNo='
download_base_url = 'http://down.znds.com'
re_compile = '/apk/tv/'
re_compile_2 = 'http://down.znds.com/getdownurl/'

url_save_path = './url_tv_apks_education.txt'

spacer = ' '

def parser_apks(count = 0):
    res_parser = {}
    page_num = 1

    try:
        while count:
            status = count
            wbdata = requests.get(url+str(page_num)).text
            print("page: "+str(page_num))

            soup = BeautifulSoup(wbdata, 'html.parser')
            divs = soup.body.find_all("h2")
            for div in divs:
                #print(div.next)
                link = div.next.attrs['href']
                download_page_link = download_base_url + link
                download_page = requests.get(download_page_link).text
                soup_download = BeautifulSoup(download_page, "html.parser")
                download_link = soup_download.find("a", href = re.compile(re_compile_2))
                try:
                    download_url = download_link.attrs['href']
                    tag = div.next.next
                    if download_url not in res_parser.values():
                        res_parser[tag] = download_url
                        count = count - 1
                except AttributeError:
                    print('no attrs href')

                if count == 0:
                    break
            if count > 0:
                if status != count:
                    page_num = page_num + 1
                else:
                    break
    except requests.exceptions.ConnectionError:
        print('no this page or exceed')

    print('total urls:'+str(len(res_parser)))
    return res_parser

def craw_urls(count = 1, save_path = './tv_apks.txt'):
    res_dic = parser_apks(count)

    file_tv_apks = open(url_save_path, 'a')
    for apk in res_dic.keys():
        file_tv_apks.write(str(apk)+spacer+str(res_dic[apk])+'\n')

def craw_apks (count = 1, save_path = './apk/'):
    res_dic = parser_apks(count)

    for apk in res_dic.keys():
        print("downloading:"+apk)
        urllib.request.urlretrieve(res_dic[apk], save_path+apk+".apk")

if __name__ == "__main__":
    #craw_apks(100)
    craw_urls(1000)