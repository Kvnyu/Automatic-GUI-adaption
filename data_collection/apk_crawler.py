#coding: utf-8
import requests
import os

store_path = '..\preprocessed_data\selected_huawei\\apps\\'
prefix_apk = 'tv_'

def crawl_apk(url_path):
    # Open anzhi_url file
    file = open(url_path, encoding='utf-8')
    data = file.readlines()
    count = 0
    for i in data:
        # i: 腾讯视频TV http://down.znds.com/getdownurl/?s=L2Rvd24vMjAyMDEwMjgvdHhzcDE2MTU4XzYuMi4wLjEwMDdfZGFuZ2JlaS5hcGs=
        line = i.split(" ")
        #apk name like: 'Tone it up', 'I cast'
        if len(line) > 2:
            apk_name = " ".join(line[:-1])
        else:
            apk_name = line[0]

        #deal with unstandard names
        apk_name = apk_name.replace('<b>', '')
        apk_name = apk_name.replace('</b>', '')

        #abc\n --> abc
        download_link = line[-1][:-1]
        download_dir = store_path + apk_name

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        apk_path = download_dir + '/' + prefix_apk + apk_name + '.apk'
        if os.path.exists(apk_path):
            fsize = os.path.getsize(apk_path)
            if fsize > 0:
                print('apk has downloaded: '+apk_path)
                count += 1
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

    # Closing file
    file.close()

if __name__ == '__main__':
    crawl_apk('..\preprocessed_data\selected_huawei\\tv_urls.txt')