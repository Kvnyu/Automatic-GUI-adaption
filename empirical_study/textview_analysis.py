import os
import json
import shutil
from empirical_study.GUI_frequency_count import parse_view
import difflib
spacer = '     |||     '

android_dir = '..\preprocessed_data\empirical_study\pairs\\android'
tv_dir = '..\preprocessed_data\empirical_study\pairs\\tv'
resluts_dir = '..\preprocessed_data\empirical_study\pairs\\android-tv'
root = '..\preprocessed_data\empirical_study\pairs'

# 2020-11-16_104643_2020-11-16_105627_screen_2020-11-16_104643
def find_corresponding_GUI_pairs(android_dir, tv_dir, resluts_dir):
    if not os.path.exists(resluts_dir):
        os.mkdir(resluts_dir)
    an_json_files = []
    tv_json_files = []
    for root, dirs, files in os.walk(android_dir):
        for file in files:
            suffix = file.split('.')[-1]
            if suffix == 'json':
                an_json_files.append(file)

    for root, dirs, files in os.walk(tv_dir):
        for file in files:
            suffix = file.split('.')[-1]
            if suffix == 'json':
                tv_json_files.append(file)

    corresponding_textviews_list = []
    corresponding_layouts_list = []
    for an_json in an_json_files:
        for tv_json in tv_json_files:
            an_json_clips = an_json.split('_')
            an_name = "".join(an_json_clips[:4])
            tv_json_clips = tv_json.split("_")
            tv_name = "".join(tv_json_clips[0:4])

            if an_name == tv_name:
                pairs_dir = os.path.join(resluts_dir, an_name)
                if not os.path.exists(pairs_dir):
                    os.mkdir(pairs_dir)
                an_json_path = os.path.join(android_dir, an_json)
                tv_json_path = os.path.join(tv_dir, tv_json)
                shutil.copy(an_json_path, os.path.join(pairs_dir, an_json))
                shutil.copy(tv_json_path, os.path.join(pairs_dir, tv_json))

                an_textviews, an_views = get_GUIs_from_json(an_json_path)
                tv_textviews, tv_views = get_GUIs_from_json(tv_json_path)

                for an_textview in an_textviews:
                    for tv_textview in tv_textviews:
                        if an_textview == tv_textview:
                            continue
                        an_textview_text = (an_textview.split(spacer)[3]).replace('\n', '')
                        tv_textview_text = (tv_textview.split(spacer)[3]).replace('\n', '')
                        similarity = difflib.SequenceMatcher(None, tv_textview_text, an_textview_text).quick_ratio()
                        if similarity > 0.9:
                            corresponding_textviews_list.append(an_textview)
                            corresponding_textviews_list.append(tv_textview)
                            corresponding_textviews_list.append('\n')

                            an_parent_id = int(an_textview.split(spacer)[-1])
                            tv_parent_id = int(tv_textview.split(spacer)[-1])

                            an_parent_layout = trace_layout(an_parent_id, an_views)
                            tv_parent_layout = trace_layout(tv_parent_id, tv_views)
                            corresponding_layouts_list.append(parse_view(an_parent_layout, GUI_type='Layout'))
                            corresponding_layouts_list.append(parse_view(tv_parent_layout, GUI_type='Layout'))
                            corresponding_layouts_list.append('\n')

    corresponding_textviews_path = os.path.join(resluts_dir[:resluts_dir.rindex('\\')], 'corresponding_textviews.txt')
    corresponding_layouts_path = os.path.join(resluts_dir[:resluts_dir.rindex('\\')], 'corresponding_layout.txt')
    with open(corresponding_textviews_path, 'w', encoding='utf8') as f_textview, open(corresponding_layouts_path, 'w', encoding='utf8') as f_layout:
        for textview in corresponding_textviews_list:
            f_textview.write(textview)
        for layout in corresponding_layouts_list:
            f_layout.write(layout)
    return corresponding_textviews_list, corresponding_layouts_list


def get_GUIs_from_json(json_file_path, GUI_type='TextView'):
    with open(json_file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
        # print(data['views'].decode('utf-8'))
        views = data['views']
        tag = data['tag']
        state_str = data['state_str']
        foreground_activity = data['foreground_activity']
        return views_parser(views, GUI_type)


def views_parser(views, GUI_type='TextView'):
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

if __name__ == '__main__':
    find_corresponding_GUI_pairs(android_dir, tv_dir, resluts_dir)