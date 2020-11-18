import json
import matplotlib.pyplot as plt
import os
import shutil

tv_json_file_path = 'results\\apks\\1\\aqiyi\qiyiguo_official10.11.2.apk\states\state_2020-11-16_103235.json'
android_json_file_path = 'results\\apks\\1\\aqiyi\iqiyi_20236.apk\states\state_2020-11-16_102502.json'

def parse_droidbot_json(json_file_path):
    print('parse begin...')
    bounds = []
    texts = []
    fig = plt.figure('Andoird app layout', dpi=500)
    ax1 = fig.add_subplot(1,1,1)

    ax1.xaxis.set_ticks_position('top')  # put x axis on the top
    #ax1.invert_xaxis()  # invert x axis
    #ax1.invert_yaxis()

    with open(json_file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
        #print(data['views'].decode('utf-8'))
        views = data['views']
        tag = data['tag']
        state_str = data['state_str']
        plt.xlim(views[0]['bounds'][0][0], views[0]['bounds'][1][0])
        plt.ylim(views[0]['bounds'][1][1], views[0]['bounds'][0][1])

        for view in views:
            text = view['text']
            if text != None:
                texts.append(text)

            class_type = view['class']
            # if 'View' not in class_type:
            #     continue
            if 'Layout' in class_type:
                continue
            bounds = view['bounds']
            bounds.append(view['bounds'])
            ax1.add_patch(plt.Rectangle(
                bounds[0],
                bounds[1][0] - bounds[0][0],
                bounds[1][1] - bounds[0][1],
                fill=False,
                edgecolor='red'
            ))

    #plt.show()
    plt.savefig(json_file_path+'.png')
    return bounds, texts


def draw_rectangle(bounds):
    print(bounds)

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
    print(count)
    if count * 5 > min_len:
        return True
    else:
        return False


def find_corresponding_snapshot(android_json_path, tv_json_path, root_dir, an_dir, tv_dir):
    tv_bounds, tv_texts = parse_droidbot_json(tv_json_path)
    android_bounds, android_texts = parse_droidbot_json(android_json_path)
    status = check_similarity(tv_texts, android_texts)
    if status == True:
        copy_file(android_json_path, tv_json_path, root_dir, an_dir, tv_dir)
    else:
        return False

def copy_file(android_json_path, tv_json_path, root_dir, an_dir, tv_dir):
    an_name = ((android_json_path.split('\\')[-1]).split('.')[0])[6:]
    tv_name = ((tv_json_path.split('\\')[-1]).split('.')[0])[6:]

    coresponding_snapshots_dir = os.path.join(root_dir, 'coresponding_snapshots_dir', an_name)
    if not os.path.exists(coresponding_snapshots_dir):
        os.makedirs(coresponding_snapshots_dir)

    for root, dirs, files in os.walk(an_dir, topdown=False):
        for file in files:
            if an_name in file:
                shutil.copy(os.path.join(an_dir, file), os.path.join(coresponding_snapshots_dir, file))

    for root, dirs, files in os.walk(tv_dir, topdown=False):
        for file in files:
            if tv_name in file:
                shutil.copy(os.path.join(tv_dir, file), os.path.join(coresponding_snapshots_dir, file))


if __name__=='__main__':
    # tv_bounds, tv_texts = parse_droidbot_json(tv_json_file_path)
    # _, android_texts = parse_droidbot_json(android_json_file_path)
    # print(check_similarity(tv_texts, android_texts))

    find_corresponding_snapshot(android_json_file_path, tv_json_file_path, 'results\\apks\\1\\aqiyi',
                                'results\\apks\\1\\aqiyi\iqiyi_20236.apk\states', 'results\\apks\\1\\aqiyi\qiyiguo_official10.11.2.apk\states')