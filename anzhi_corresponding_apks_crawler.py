import json
import requests
import os
import difflib
from  apk_crawler import store_path

spacer = '     |||     '

tv_corresponding_app_path = './tv_corresponding_apps.txt'
tv_dic = open('./tv_dic.txt', encoding='gbk').readlines()
tv_corresponding_apps = open(tv_corresponding_app_path, 'a+', encoding='gbk')

def download(file_path):
    # returns JSON object as
    # a dictionary
    file = open(file_path, encoding='gbk')
    data = json.load(file)
    count = 0

    for i in data:
        apk_name = i['name']
        # deal with unstandard names
        apk_name = apk_name.replace('<b>', '')
        apk_name = apk_name.replace('</b>', '')

        tv_app = check_tv_dic(apk_name, tv_dic)

        #gbk can not convert '\xa0'
        # apk_name = apk_name.replace(u'\xa0', u' ')
        # apk_name = apk_name.replace(u'\u0643', u' ')
        # apk_name = apk_name.replace(u'\u06c6', u' ')
        # apk_name = apk_name.replace(u'\u0631', u' ')
        # apk_name = apk_name.replace(u'\u2122', u' ')
        # apk_name = apk_name.replace(u'\u200b', u' ')
        # apk_name = apk_name.replace(u'\u2022', u' ')
        # apk_name = apk_name.replace(u'\ufeff', u' ')
        apk_name = apk_name.encode('gbk', 'ignore').decode('gbk')

        if tv_app == 0:
            print(apk_name+": no corresponding tv app")
            continue
        else:
            # tv_app = tv_app.replace(u'\xa0', u' ')
            # tv_app = tv_app.replace(u'\u0643', u' ')
            # tv_app = tv_app.replace(u'\u06c6', u' ')
            # tv_app = tv_app.replace(u'\u0631', u' ')
            # tv_app = tv_app.replace(u'\u2122', u' ')
            # tv_app = tv_app.replace(u'\u200b', u' ')
            # tv_app = tv_app.replace(u'\u2022', u' ')
            # tv_app = tv_app.replace(u'\ufeff', u' ')
            tv_app = tv_app.encode('gbk', 'ignore').decode('gbk')
            print('find corresponding tv app:' + tv_app + " and "+ apk_name)

        download_link = i['download']
        download_dir = store_path + tv_app

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        apk_path = download_dir + '/' + apk_name + '.apk'

        tv_corresponding_apps.write(tv_app + spacer + apk_name + spacer + download_dir + '\n')

        if os.path.exists(apk_path):
            fsize = os.path.getsize(apk_path)
            if fsize > 0:
                print('apk has downloaded: '+apk_path)
                count += 1
                print(str(len(data)) + '/' + str(count))
                continue
            else:
                print('0 kb apk, delete '+apk_path)
                os.remove(apk_path)
        try:
            with open(apk_path, 'wb') as file:
                file = open(apk_path, 'wb')
                response = requests.get(download_link, timeout=10, stream=True)
                print('downloading', apk_name, 'now...')
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                count += 1
                print(str(len(data))+'/'+str(count))
        except ConnectionError:
            print('Failed to establish a new connection:'+download_link)
            count += 1
        except TimeoutError:
            print('TimeoutError:' + download_link)
            count += 1
        except requests.exceptions.ConnectTimeout:
            print('requests.exceptions.ConnectTimeout:'+download_link)
            count += 1
        except OSError:
            print('OSError:' + apk_path)
            count += 1

    file.close()

def check_tv_dic(app_name, tv_dic):
    similarity = 0
    for line in tv_dic:
        line = line[:-1]
        similarity = difflib.SequenceMatcher(None, app_name, line).quick_ratio()
        if similarity > 0.6:
            return line

    return 0


if __name__=='__main__':
    #Opening JSON file
    for root, dirs, files in os.walk("./anzhi_url", topdown=False):
        for file_path in files:
            download(root+'/'+file_path)

    # Closing file
    print('total coressponding apks:'+str(len(tv_corresponding_apps.readlines())))
    tv_corresponding_apps.close()