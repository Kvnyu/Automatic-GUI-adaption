#coding = utf-8
import json
import requests
import os
import difflib
from  data_collection.apk_crawler import store_path

spacer = '     |||     '
min_apk_size = 100*1024
tv_corresponding_app_path = '..\preprocessed_data\selected_huawei\\apps\\android_tv_apps.txt'
tv_dic = open('..\preprocessed_data\selected_huawei\\android_dic.txt', encoding='utf-8').readlines()
tv_corresponding_apps = open(tv_corresponding_app_path, 'a+', encoding='utf-8')

def traverse(file_path):
    # returns JSON object as
    # a dictionary
    file = open(file_path, encoding='utf-8')
    data = json.load(file)
    count = 0

    for i in data:
        apk_name = i['name']
        # deal with unstandard names
        apk_name = apk_name.replace('<b>', '')
        apk_name = apk_name.replace('</b>', '')

        tv_app = check_android_dic(apk_name, tv_dic)

        #apk_name = apk_name.encode('gbk', 'ignore').decode('gbk')

        try:
            if tv_app == 0:
                #print(apk_name+": no corresponding tv app")
                continue
            else:
                #tv_app = tv_app.encode('gbk', 'ignore').decode('gbk')
                print('find corresponding tv app:' + tv_app + " and "+ apk_name)
        except UnicodeError as e:
            print('UnicodeEncodeError...')

        download_link = i['download']
        download_dir = store_path + tv_app

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        apk_path = os.path.join(download_dir, tv_app + '.apk')

        tv_corresponding_apps.write(tv_app + spacer + apk_name + spacer + download_dir + '\n')

        if os.path.exists(apk_path):
            fsize = os.path.getsize(apk_path)
            if fsize > min_apk_size:
                print('apk has downloaded: '+apk_path)
                count += 1
                print(str(len(data)) + '/' + str(count))
                continue
            else:
                print('less than 100 kb apk, delete '+apk_path)
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


def check_dic(app_name, tv_dic):
    similarity = 0
    for line in tv_dic:
        line = line[:-1]
        similarity = difflib.SequenceMatcher(None, app_name, line).quick_ratio()
        if similarity > 0.8:
            return line

    return 0


def check_android_dic(app_name, tv_dic):
    for line in tv_dic:
        line = line[:-1]
        if app_name in line:
            return line

    return 0


if __name__=='__main__':
    #Opening JSON file
    for root, dirs, files in os.walk("..\preprocessed_data\\anzhi_url", topdown=False):
        for file_path in files:
            traverse(os.path.join(root, file_path))

    # Closing file
    print('total coressponding apks:'+str(len(tv_corresponding_apps.readlines())))
    tv_corresponding_apps.close()