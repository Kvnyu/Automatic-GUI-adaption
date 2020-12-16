import json
import matplotlib.pyplot as plt
import os
import PIL.Image as img
import shutil

json_file_path = '..\preprocessed_data\\test_data\\state_2020-12-12_103956.json'
img_path = '..\preprocessed_data\\test_data\\screen_2020-12-12_103956.jpg'

multiplication_factor = 0.8
spacer = '     |||     '

dir1 = '..\preprocessed_data\GUI_division\\app_market'
dir2 = '..\preprocessed_data\GUI_division\\app_media'
dir3 = '..\preprocessed_data\GUI_division\\app_smart'


def GUI_division(json_file_path, img_path, multiplication_factor):
    #print('parse begin...')

    save_dir = img_path + '_blocks'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    json_name = json_file_path[img_path.rindex('\\') + 1:]
    img_name = img_path[img_path.rindex('\\') + 1:]
    bounds_all = []
    texts = []

    with open(json_file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
        #print(data['views'].decode('utf-8'))
        views = data['views']
        tag = data['tag']
        state_str = data['state_str']
        foreground_activity = data['foreground_activity']

        x_min = views[0]['bounds'][0][0]
        x_max = views[0]['bounds'][1][0]
        y_min = views[0]['bounds'][0][1]
        y_max = views[0]['bounds'][1][1]

        if y_max > x_max:
            fig = plt.figure(figsize=(10, 15))
        else:
            fig = plt.figure(figsize=(15, 10))
        ax1 = fig.add_subplot(1, 1, 1)

        # put x axis on the top
        ax1.xaxis.set_ticks_position('top')
        plt.axis([x_min, x_max, y_max, y_min])

        len_views = len(views)
        if len_views < 0:
            return
        view_root = views[0]
        class_type = view_root['class']
        size = view_root['size'].split('*')
        size_1 = int(size[0])
        size_2 = int(size[1])

        leaves = []
        for view in views:
            child_count = view['child_count']
            if child_count == 0:
                leaves.append(view)

        views_str = []
        blocks = []
        for leaf in leaves:
            block = trace_view(leaf, size_1, size_2, views, views_str, multiplication_factor)
            if block != None:
                blocks.append(block)

        blocks, blocks_bounds = views_filter(blocks, x_min, y_min, x_max, y_max)

        color = ['red', 'blue', 'black', 'pink', 'yellow']
        j = 0
        for block in blocks:
            bounds = block['bounds']
            ax1.add_patch(plt.Rectangle(
                bounds[0],
                bounds[1][0] - bounds[0][0],
                bounds[1][1] - bounds[0][1],
                fill=False,
                edgecolor=color[j]
            ))
            j =j + 1
            if j >= len(color):
                j = 0
    #plt.show()

    GUI_skeleton_save_path = os.path.join(save_dir, json_name+'.png')
    plt.savefig(GUI_skeleton_save_path)
    shutil.copy(img_path, os.path.join(save_dir, img_name))
    fig.canvas.flush_events()
    plt.close()

    im = img.open(img_path)
    print(im.size)
    suffix = img_name.split('.')[-1]

    for i in range(len(blocks_bounds)):
        box = (blocks_bounds[i][0][0], blocks_bounds[i][0][1], blocks_bounds[i][1][0], blocks_bounds[i][1][1])
        ng = im.crop(box)
        #name = img_path[img_path.rindex('\\') + 1:]
        save_path = os.path.join(save_dir, str(i) + '_' + img_name)
        ng = ng.convert('RGB')
        ng.save(save_path)
    return bounds_all


def trace_view(view, max_length, max_height, views, views_str, multiplication_factor=0.9):
    size = view['size']
    size = size.split('*')
    size_1 = int(size[0])
    size_2 = int(size[1])

    if size_1 < 0 or size_2 < 0:
        return None

    view_str = simple_parse_view(view, spacer)
    if view_str in views_str:
        return None
    else:
        views_str.append(view_str)

    if size_1 >= max_length * multiplication_factor:
        return view
    else:
        parent = view['parent']
        if parent == -1:
            return None

        return trace_view(views[parent], max_length, max_height, views, views_str, multiplication_factor)


def views_filter(views, x_min, y_min, x_max, y_max):
    blocks = []
    blocks_bounds_str = []
    blocks_bounds = []

    for view in views:
        bounds = view['bounds']
        if bounds[0][0] == bounds[1][0] or bounds[0][1] == bounds[1][1]:
            continue

        bounds_str = str(bounds)
        if bounds_str not in blocks_bounds_str:
            blocks_bounds_str.append(bounds_str)
            blocks_bounds.append(bounds)
            blocks.append(view)

    blocks_temp = []
    blocks_bounds_temp = []
    for block, block_bound in zip(blocks, blocks_bounds):
        child_count = block['child_count']
        clss_type = block['class']
        blocks_temp.append(block)
        blocks_bounds_temp.append(block_bound)

    return blocks_temp, blocks_bounds_temp


def align_picture_xml_pairs(pictures, xmls):
    pairs = []
    for picture in pictures:
        # screen_2020-12-16_101746.jpg, state_2020-12-16_101746.json
        pair = []
        pair.append(picture)
        picture_name = (picture.split('_')[2]).split('.')[0]
        for xml in xmls:
            if picture_name in xml:
                pair.append(xml)
                pairs.append(pair)
                break

    return pairs


def traverse_GUI_division(dir, multiplication_factor):
    xmls = []
    pictures = []
    for file in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, file)):
            if 'jpg' in file or 'png' in file:
                pictures.append(file)
            else:
                if 'json' in file:
                    xmls.append(file)

    pairs = align_picture_xml_pairs(pictures, xmls)
    for pair in pairs:
        img_path = os.path.join(dir, pair[0])
        xml_path = os.path.join(dir, pair[1])
        GUI_division(xml_path, img_path, multiplication_factor)


def simple_parse_view(view, spacer):
    class_type = view['class']
    if class_type == None:
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
    features = features.replace('\n', '')
    features = features + '\n'
    return features


if __name__=='__main__':
    # GUI_division(json_file_path, img_path, 0.7)
    traverse_GUI_division(dir1, multiplication_factor)