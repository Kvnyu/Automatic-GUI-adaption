import json
import matplotlib.pyplot as plt
import os
import shutil
from matplotlib.pyplot import MultipleLocator
from GUI_collection.collect_snapshots import copy_snapshot_json, check_main_activity, check_an_tv_result
empirical_study_dir = 'preprocessed_data\empirical_study\pairs'

def parse_droidbot_json(json_file_path):
    #print('parse begin...')
    bounds_all = []
    texts = []
    is_main_activity = False

    with open(json_file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
        #print(data['views'].decode('utf-8'))
        views = data['views']
        tag = data['tag']
        state_str = data['state_str']
        foreground_activity = data['foreground_activity']
        is_main_activity = check_main_activity(foreground_activity)

        x_min = views[0]['bounds'][0][0]
        x_max = views[0]['bounds'][1][0]
        y_min = views[0]['bounds'][0][1]
        y_max = views[0]['bounds'][1][1]

        if y_max > x_max:
            fig = plt.figure(figsize=(10, 15))
        else:
            fig = plt.figure(figsize=(15, 10))
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.xaxis.set_ticks_position('top')  # put x axis on the top

        plt.axis([x_min, x_max, y_max, y_min])

        current_color = 'red'
        status_zero = True
        for view in views:
            text = view['text']
            if text != None:
                texts.append(text)

            size = view['size'].split('*')
            size_1 = int(size[0])
            size_2 = int(size[1])
            if not status_zero:
                if size_1 >= x_max or size_1 >= y_max:
                    if current_color == 'red':
                        current_color = 'blue'
                    else:
                        current_color = 'red'
                if size_2 >= x_max or size_2 >= y_max:
                    if current_color == 'red':
                        current_color = 'blue'
                    else:
                        current_color = 'red'

            class_type = view['class']

            if class_type == None:
                continue
            if 'View' not in class_type:
                continue
            if 'Layout' in class_type:
                continue

            bounds = view['bounds']
            bounds_all.append(view['bounds'])
            ax1.add_patch(plt.Rectangle(
                bounds[0],
                bounds[1][0] - bounds[0][0],
                bounds[1][1] - bounds[0][1],
                fill=False,
                edgecolor=current_color
            ))
            status_zero = False

    #plt.show()
    plt.savefig(json_file_path+'.png')
    fig.canvas.flush_events()
    plt.close()
    return bounds_all, texts, is_main_activity


def check_similarity(texts1, texts2):
    count = 0
    len1 = len(texts1)
    len2 = len(texts2)
    min_len = min(len1, len2)
    if len1 < len2:
        for text1 in texts1:
            if text1 in texts2:
                #print(text1)
                count += 1
    else:
        for text2 in texts2:
            if text2 in texts1:
                count += 1
    if count * 5 > min_len:
        print('the same texts: ' + str(count))
        return True
    else:
        return False

def find_corresponding_snapshot(android_json_path, tv_json_path, root_dir, an_dir, tv_dir):
    tv_bounds, tv_texts, an_is_main = parse_droidbot_json(tv_json_path)
    android_bounds, android_texts, tv_is_main = parse_droidbot_json(android_json_path)

    an_name = ((android_json_path.split('\\')[-1]).split('.')[0])[6:]
    tv_name = ((tv_json_path.split('\\')[-1]).split('.')[0])[6:]

    if an_is_main:
        dst = os.path.join(root_dir, 'main_activity', 'android')
        copy_snapshot_json(an_name, dst, an_dir)
    if tv_is_main:
        dst = os.path.join(root_dir, 'main_activity', 'tv')
        copy_snapshot_json(tv_name, dst, tv_dir)

    status = check_similarity(tv_texts, android_texts)
    if status == True:
        #copy_file(android_json_path, tv_json_path, root_dir, an_dir, tv_dir)
        dst = os.path.join(root_dir, 'coresponding_snapshots_dir', an_name + '+' +tv_name)
        copy_snapshot_json(an_name, dst, an_dir)
        copy_snapshot_json(tv_name, dst, tv_dir)

        #collect corresponding snapshots
        an_dst_corresponding_snapshots = os.path.join(empirical_study_dir, 'android')
        tv_dst_corresponding_snapshots = os.path.join(empirical_study_dir, 'tv')
        copy_snapshot_json(an_name, an_dst_corresponding_snapshots, an_dir, new_name=an_name+'_'+tv_name)
        copy_snapshot_json(tv_name, tv_dst_corresponding_snapshots, tv_dir, new_name=an_name+'_'+tv_name)

    else:
        return False

def traverse_snapshots(an_dir, tv_dir, root_dir):
    print('traverse: '+root_dir)
    an_json_files = []
    tv_json_files = []
    for root, dirs, files in os.walk(an_dir):
        for file in files:
            suffix = file.split('.')[-1]
            if suffix == 'json':
                an_json_files.append(os.path.join(root, file))

    for root, dirs, files in os.walk(tv_dir):
        for file in files:
            suffix = file.split('.')[-1]
            if suffix == 'json':
                tv_json_files.append(os.path.join(root, file))

    #print(len(an_json_files))

    for tv_json_file in tv_json_files:
        for an_json_file in an_json_files:
            find_corresponding_snapshot(an_json_file, tv_json_file, root_dir, an_dir, tv_dir)


def split_views():
    print()

def traverse_all_dataset(path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if check_an_tv_result(os.path.join(root, dir)):
                #print('valid')
                an_states = os.path.join(root, dir, dir+'.apk', 'states')
                tv_states = os.path.join(root, dir, 'tv_'+dir+'.apk', 'states')
                traverse_snapshots(an_states, tv_states, os.path.join(root, dir))
            else:
                continue



if __name__=='__main__':
    #json_path = 'results\\apks\\1\\aqiyi\qiyiguo_official10.11.2.apk\state_2020-11-16_103409.json'
    #json_path = 'results\\apks\\1\\aqiyi\iqiyi_20236.apk\state_2020-11-16_102435.json'
    #tv_bounds, tv_texts, _ = parse_droidbot_json(json_path)
    # _, android_texts = parse_droidbot_json(android_json_file_path)
    # print(check_similarity(tv_texts, android_texts))

    # find_corresponding_snapshot(android_json_file_path, tv_json_file_path, 'results\\apks\\1\\aqiyi',
    #                             'results\\apks\\1\\aqiyi\iqiyi_20236.apk\states', 'results\\apks\\1\\aqiyi\qiyiguo_official10.11.2.apk\states')

    #traverse_snopshot('results\\apks\\1\\aqiyi\iqiyi_20236.apk\states', 'results\\apks\\1\\aqiyi\qiyiguo_official10.11.2.apk\states', 'results\\apks\\1\\aqiyi')

    traverse_all_dataset('preprocessed_data\selected_apps\\1')
    traverse_all_dataset('preprocessed_data\selected_apps\\2')
    traverse_all_dataset('preprocessed_data\selected_apps\\3')
    traverse_all_dataset('preprocessed_data\high_similarity_apps')
    #traverse_all_dataset('selected_apps')