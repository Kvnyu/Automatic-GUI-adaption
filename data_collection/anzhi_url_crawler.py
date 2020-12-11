import os
import requests
from bs4 import BeautifulSoup
import json


# crawl apps in all categories, maximum page 1000
def getSoftItems(url):
    num = 1
    items = list()
    old = '_1_hot'
    session = requests.session()
    try:
        while True:
            new = '_'+str(num)+'_hot'
            url = url.replace(old, new)
            print(url)
            html = session.get(url).text
            soup = BeautifulSoup(html, 'html.parser')
            app_names = soup.select('span.app_name>a')
            if not app_names or num >= 1500:  # maximum page 1000
                break
            links = [item['href'] for item in app_names if item and 'href'in item.attrs]
            items.extend(['http://www.anzhi.com' + i for i in links])
            num = num + 1
            old = new
    except Exception as e:
        print(e)
    print("{}, crawl {} url。".format(url, len(items)))
    return items


# http://www.anzhi.com//sort_45_3_hot.html
# get all categories's urls
def getCatURL():
    url = 'http://www.anzhi.com/widgetcatetag_1.html'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    cats = soup.select('a')
    cat_list = [i['href'] for i in cats if 'tsort' not in i['href']]
    newCat = ["http://www.anzhi.com" + i for i in cat_list]
    return newCat


# record the detail of apps
def getSoftJson(url):
    global number
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select('div.detail_line > h3')[0].text
        infos = soup.select('#detail_line_ul > li')
        soft_id = soup.select('div.detail_down > a')[0]['onclick'][9:-2]
        js = {}
        js['name'] = title
        js['cat'] = infos[0].text.split('：')[-1]
        js['download_cnt'] = infos[1].text.split('：')[-1]
        js['time'] = infos[2].text.split('：')[-1]
        js['size'] = infos[3].text.split('：')[-1]
        js['sys'] = infos[4].text.split('：')[-1]
        js['download'] = f"http://www.anzhi.com/dl_app.php?s={soft_id}&n=5"
        return js
    except Exception as e:
        print("an error occur in extracting json：{}".format(e))
    return None



def SaveApkToJSON(json_root_dir):
    # params: json_root_dir json the save path of json
    cats = getCatURL()  # get all categories in anzhi app store

    for index1, i in enumerate(cats):
        # if index1 <= 3:
        #     continue
        all_links = getSoftItems(i)  # get urls
        all_json = list()
        for index2, link in enumerate(all_links):
            print("connecting index：{}，connect... ：{}".format(index2, link))
            js = getSoftJson(link)
            if js:
                all_json.append(js)
        file_path = json_root_dir + "/apk_link_" + str(index1) + ".json"
        print("save json path: ，", file_path)
        with open(file_path, mode='w+') as f:
            json.dump(all_json, f, indent=4)

        print("index {}，json has saved ".format(index1))


# save all urls from anzhi app store in json files
if __name__ == "__main__":
    json_root_dir = os.path.abspath(r"../preprocessed_data/anzhi_url")
    if not os.path.exists(json_root_dir):
        os.makedirs(json_root_dir)
    SaveApkToJSON(json_root_dir)

