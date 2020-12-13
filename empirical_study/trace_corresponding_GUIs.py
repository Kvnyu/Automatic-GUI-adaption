import os
import json
import shutil
from empirical_study.GUI_frequency_count import parse_view
import difflib
import matplotlib.pyplot as plt
from empirical_study.utils import parse_view, get_GUIs_from_json, trace_layout, draw_GUI_skeleton
from empirical_study.utils import spacer
from GUI_collection.collect_snapshots import copy_snapshot_json_skeleton

android_dir = '..\preprocessed_data\empirical_study\pairs\\android'
tv_dir = '..\preprocessed_data\empirical_study\pairs\\tv'
resluts_dir = '..\preprocessed_data\empirical_study\pairs\\android-tv'
root = '..\preprocessed_data\empirical_study\pairs'


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

    corresponding_views_list = []
    corresponding_layouts_list = []

    # 2020-11-16_104643_2020-11-16_105627_screen_2020-11-16_104643, check 2020-11-16_104643_2020-11-16_105627
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
                an_json_dst = os.path.join(pairs_dir, an_json)
                copy_snapshot_json_skeleton(an_json.split('.')[0], pairs_dir, android_dir)
                #shutil.copy(an_json_path, an_json_dst)
                tv_json_dst = os.path.join(pairs_dir, tv_json)
                #shutil.copy(tv_json_path, tv_json_dst)
                copy_snapshot_json_skeleton(tv_json.split('.')[0], pairs_dir, tv_dir, new_name='tv_')

                # find corresponding GUI pairs
                an_views_lines, an_views = get_GUIs_from_json(an_json_path, GUI_type='View')
                tv_views_lines, tv_views = get_GUIs_from_json(tv_json_path, GUI_type='View')

                draw_an_views = []
                draw_tv_views = []
                draw_an_views.append(an_views[0])
                draw_tv_views.append(tv_views[0])

                for an_view in an_views_lines:
                    for tv_view in tv_views_lines:
                        if an_view == tv_view:
                            continue
                        an_textview_text = (an_view.split(spacer)[6]).replace('\n', '')
                        tv_textview_text = (tv_view.split(spacer)[6]).replace('\n', '')
                        similarity = difflib.SequenceMatcher(None, tv_textview_text, an_textview_text).quick_ratio()
                        if similarity > 0.9:
                            if an_view in corresponding_views_list and tv_view in corresponding_views_list:
                                continue
                            corresponding_views_list.append(an_view)
                            corresponding_views_list.append(tv_view)
                            corresponding_views_list.append('\n')

                            # utilize the textview to identify the layout that contains the textview
                            an_parent_id = int(an_view.split(spacer)[3])
                            tv_parent_id = int(tv_view.split(spacer)[3])
                            an_parent_layout = trace_layout(an_parent_id, an_views)
                            tv_parent_layout = trace_layout(tv_parent_id, tv_views)
                            an_line = parse_view(an_parent_layout, GUI_type='Layout')
                            tv_line = parse_view(tv_parent_layout, GUI_type='Layout')
                            if an_line in corresponding_layouts_list and tv_line in corresponding_layouts_list:
                                continue
                            corresponding_layouts_list.append(an_line)
                            corresponding_layouts_list.append(tv_line)
                            corresponding_layouts_list.append('\n')

                            draw_an_views.append(an_parent_layout)
                            draw_tv_views.append(tv_parent_layout)

                # draw_GUI_skeleton(plt, draw_an_views, an_json_dst)
                # draw_GUI_skeleton(plt, draw_tv_views, tv_json_dst)

    corresponding_textviews_path = os.path.join(resluts_dir[:resluts_dir.rindex('\\')], 'corresponding_views.txt')
    corresponding_layouts_path = os.path.join(resluts_dir[:resluts_dir.rindex('\\')], 'corresponding_layout.txt')
    with open(corresponding_textviews_path, 'w', encoding='utf8') as f_view, open(corresponding_layouts_path, 'w', encoding='utf8') as f_layout:
        for textview in corresponding_views_list:
            f_view.write(textview)
        for layout in corresponding_layouts_list:
            f_layout.write(layout)

    return corresponding_views_list, corresponding_layouts_list


if __name__ == '__main__':
    find_corresponding_GUI_pairs(android_dir, tv_dir, resluts_dir)