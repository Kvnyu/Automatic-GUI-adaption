import json
import matplotlib.pyplot as plt
import os
from empirical_study.utils import simple_parse_view
import PIL.Image as img
import copy
import numpy as np

json_file_path = '..\preprocessed_data\\test_data\\2020-11-16_135334_2020-11-16_134217_state_2020-11-16_135334.json'
img_path = '..\preprocessed_data\\test_data\\2020-11-16_135334_2020-11-16_134217_screen_2020-11-16_135334.jpg'

def GUI_division(json_file_path):
    #print('parse begin...')
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
        ax1.xaxis.set_ticks_position('top')  # put x axis on the top

        plt.axis([x_min, x_max, y_max, y_min])

        len_views = len(views)
        if len_views < 0:
            return
        view_0 = views[0]
        class_type = view_0['class']
        size = view_0['size'].split('*')
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
            block = trace_view(leaf, size_1, size_2, views, views_str, 0.9)
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
    plt.savefig(json_file_path+'.png')
    fig.canvas.flush_events()
    plt.close()

    im = img.open(img_path)
    print(im.size)
    suffix = img_path[img_path.rindex('.'):]
    save_dir = img_path + '_blocks'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    for i in range(len(blocks_bounds)):
        box = (blocks_bounds[i][0][0], blocks_bounds[i][0][1], blocks_bounds[i][1][0], blocks_bounds[i][1][1])
        ng = im.crop(box)
        name = img_path[img_path.rindex('\\') + 1:]
        save_path = os.path.join(save_dir, str(i) + '_' + name)
        ng = ng.convert('RGB')
        ng.save(save_path)
    return bounds_all


def trace_view(view, max_length, max_height, views, views_str, operator = 1):
    size = view['size']
    size = size.split('*')
    size_1 = int(size[0])
    size_2 = int(size[1])

    if size_1 < 0 or size_2 < 0:
        return None

    view_str = simple_parse_view(view)
    if view_str in views_str:
        return None
    else:
        views_str.append(view_str)

    if size_1 >= max_length * operator:
        return view
    else:
        parent = view['parent']
        if parent == -1:
            return None

        return trace_view(views[parent], max_length, max_height, views, views_str, operator)


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

    # for i in range(len(blocks)):
    #     for j in range(len(blocks)):
    #         if i == j:
    #             continue
    #         if blocks[i] == 0 or blocks[j] == 0:
    #             continue
    #         if blocks_bounds[i][0][0] <= blocks_bounds[j][0][0] and blocks_bounds[i][0][1] <= blocks_bounds[j][0][1]:
    #             if blocks_bounds[i][1][0] >= blocks_bounds[j][1][0] and blocks_bounds[i][1][1] >= blocks_bounds[j][1][1]:
    #                 blocks[i] = 0
    #                 blocks_bounds[i] = 0

    blocks_temp = []
    blocks_bounds_temp = []
    for block, block_bound in zip(blocks, blocks_bounds):
        child_count = block['child_count']
        clss_type = block['class']

        blocks_temp.append(block)
        blocks_bounds_temp.append(block_bound)

    return blocks_temp, blocks_bounds_temp


if __name__=='__main__':
    GUI_division(json_file_path)