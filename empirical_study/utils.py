import os
import json
spacer = '     |||     '


def parse_view(view, GUI_type):
    View_list = ['View', 'ActionBar', 'Menu', 'Gallery', 'ProgressBar', 'UI Style', 'Button', 'EditText', 'Clock', 'Picker']
    class_type = view['class']
    if class_type == None:
        return None

    if GUI_type == 'View':
        status = False
        for View in View_list:
            if View in class_type:
                status = True
        if status == False:
            return None
    else:
        if GUI_type not in class_type:
            return None

    size = view['size']
    bounds = view['bounds']
    parent = view['parent']
    child_count = view ['child_count']
    children = view['children']
    if child_count == 0:
        children = None

    text = view['text']
    if text == None:
        text = 'None'
    features = class_type + spacer + size + spacer + str(bounds) + spacer + str(parent) + spacer + str(child_count) + spacer + str(children) + spacer + text

    if 'ImageView' in class_type:
        content_free_signature = view['content_free_signature']
        features = features + spacer + content_free_signature

    features = features.replace('\n', '')
    features = features.replace('\r', '')
    features = features + '\n'
    return features


def analyze_GUIs(results_dir):
    print('analyze '+ results_dir)
    android_results_path = os.path.join(results_dir, 'android')
    tv_results_path = os.path.join(results_dir, 'tv')

    an_save_path = os.path.join(results_dir, 'android_frequency_count.txt')
    views_frequency_count(android_results_path, an_save_path)

    tv_save_path = os.path.join(results_dir, 'tv_frequency_count.txt')
    views_frequency_count(tv_results_path, tv_save_path)


def views_frequency_count(path, save_path):
    dict = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, encoding='utf8') as an_f:
                for line in an_f.readlines():
                    view = line.split(spacer)[0]
                    if dict.__contains__(view):
                        count = dict[view]
                        dict[view] = count + 1
                    else:
                        dict[view] = 1

    save_dict(dict, save_path)


def save_dict(dict, save_path):
    dict = sorted(dict.items(), key=lambda d: d[1], reverse=True)
    sum = 0
    for i in dict:
        sum += i[1]
    with open(save_path, 'w', encoding='utf-8') as f:
        for i in dict:
            line = str(i[0]) + spacer + str(i[1]) + spacer + str(i[1]/sum) + '\n'
            f.write(line)


def get_GUIs_from_json(json_file_path, GUI_type):
    with open(json_file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
        # print(data['views'].decode('utf-8'))
        views = data['views']
        tag = data['tag']
        state_str = data['state_str']
        foreground_activity = data['foreground_activity']
        return views_parser(views, GUI_type)


def views_parser(views, GUI_type):
    lines = set()
    for view in views:
        line = parse_view(view, GUI_type)
        if line != None:
            lines.add(line)

    return lines, views

def trace_layout(parent_id, views):
    if parent_id >= len(views):
        return None
    if parent_id == -1:
        return views[0]
    view = views[parent_id]
    class_type = view['class']
    if 'Layout' in class_type:
        return view
    else:
        parent_id = view['parent']
        return trace_layout(parent_id, views)


def draw_GUI_skeleton(plt, views, save_path):
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
        class_type = view['class']

        if class_type == None:
            continue
        # if 'View' not in class_type:
        #     continue
        # if 'Layout' in class_type:
        #     continue

        bounds = view['bounds']
        ax1.add_patch(plt.Rectangle(
            bounds[0],
            bounds[1][0] - bounds[0][0],
            bounds[1][1] - bounds[0][1],
            fill=False,
            edgecolor=current_color
        ))
    #plt.show()
    plt.savefig(save_path + '.png')
    fig.canvas.flush_events()
    plt.close()