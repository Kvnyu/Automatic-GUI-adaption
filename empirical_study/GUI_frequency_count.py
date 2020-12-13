import os
import json
from empirical_study.utils import parse_view, analyze_GUIs


results_dir = '..\preprocessed_data\empirical_study\\Layout'
corresponding_GUIs_dir = '..\preprocessed_data\empirical_study\pairs'


def activity_analysis(json_path):
    print()


def collect_GUIs(json_file_path, results_file_path, GUI_type='View'):
    with open(json_file_path, 'r', encoding='utf8') as f, open(results_file_path, 'a', encoding='utf-8') as result_f:
        data = json.load(f)
        # print(data['views'].decode('utf-8'))
        views = data['views']
        tag = data['tag']
        state_str = data['state_str']
        foreground_activity = data['foreground_activity']
        lines = set()
        for view in views:
            line = parse_view(view, GUI_type)
            if line != None:
                lines.add(line)

        for s in lines:
            result_f.write(s)


def traverse_collect_GUIs(path, results_dir, GUI_type = 'View'):
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            an_states = os.path.join(root, dir, dir + '.apk', 'states')
            tv_states = os.path.join(root, dir, 'tv_' + dir + '.apk', 'states')

            an_json_files = traverse_snapshots_json(an_states)
            if an_json_files != None:
                #an_results_file_path = os.path.join(root, dir, dir+'.txt')
                an_results_dir = os.path.join(results_dir, 'android')
                if not os.path.exists(an_results_dir):
                    os.mkdir(an_results_dir)
                an_results_file_path = os.path.join(an_results_dir, dir+'.txt')
                for an_json_file in an_json_files:
                    collect_GUIs(an_json_file, an_results_file_path, GUI_type=GUI_type)

            tv_json_files = traverse_snapshots_json(tv_states)
            if tv_json_files != None:
                #tv_results_file_path = os.path.join(root, dir, 'tv_'+dir+'.txt')
                tv_results_dir = os.path.join(results_dir, 'tv')
                if not os.path.exists(tv_results_dir):
                    os.mkdir(tv_results_dir)
                tv_results_file_path = os.path.join(tv_results_dir, 'tv_'+dir+'.txt')
                for tv_json_file in tv_json_files:
                    collect_GUIs(tv_json_file, tv_results_file_path, GUI_type=GUI_type)


def traverse_snapshots_json(dir):
    if not os.path.exists(dir):
        print('path does not exist: ' + dir)
        return None

    print('traverse: '+ dir)
    json_files = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            suffix = file.split('.')[-1]
            if suffix == 'json':
                json_files.append(os.path.join(root, file))

    return json_files


def traverse_corresponding_GUIs(corresponding_GUIs_dir, results_dir, GUI_type):
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)

    an_dir = os.path.join(corresponding_GUIs_dir, 'android')
    tv_dir = os.path.join(corresponding_GUIs_dir, 'tv')

    an_json_files = traverse_snapshots_json(an_dir)
    if an_json_files != None:
        # an_results_file_path = os.path.join(root, dir, dir+'.txt')
        an_results_dir = os.path.join(results_dir, 'android')
        if not os.path.exists(an_results_dir):
            os.mkdir(an_results_dir)
        an_results_file_path = os.path.join(an_results_dir, 'android_total.txt')
        for an_json_file in an_json_files:
            collect_GUIs(an_json_file, an_results_file_path, GUI_type=GUI_type)

    tv_json_files = traverse_snapshots_json(tv_dir)
    if tv_json_files != None:
        # tv_results_file_path = os.path.join(root, dir, 'tv_'+dir+'.txt')
        tv_results_dir = os.path.join(results_dir, 'tv')
        if not os.path.exists(tv_results_dir):
            os.mkdir(tv_results_dir)
        tv_results_file_path = os.path.join(tv_results_dir, 'tv_total.txt')
        for tv_json_file in tv_json_files:
            collect_GUIs(tv_json_file, tv_results_file_path, GUI_type=GUI_type)


if __name__ == '__main__':


    # collect_views('test_results\\2020-11-16_135351+2020-11-16_134217\state_2020-11-16_134217.json', 'test_results\\2020-11-16_135351+2020-11-16_134217\\tv.txt')
    # collect_views('test_results\\2020-11-16_135351+2020-11-16_134217\state_2020-11-16_135351.json', 'test_results\\2020-11-16_135351+2020-11-16_134217\\android.txt')


    # traverse_collect_GUIs('..\\preprocessed_data\high_similarity_apps', results_dir=results_dir, GUI_type='Layout')
    # traverse_collect_GUIs('..\\preprocessed_data\selected_apps\\1', results_dir=results_dir, GUI_type='Layout')
    # traverse_collect_GUIs('..\\preprocessed_data\selected_apps\\2', results_dir=results_dir, GUI_type='Layout')
    # traverse_collect_GUIs('..\\preprocessed_data\selected_apps\\3', results_dir=results_dir, GUI_type='Layout')
    # analyze_GUIs(results_dir)


    traverse_corresponding_GUIs(corresponding_GUIs_dir, corresponding_GUIs_dir+'\\results\\View', GUI_type='View')
    traverse_corresponding_GUIs(corresponding_GUIs_dir, corresponding_GUIs_dir + '\\results\\Layout', GUI_type='Layout')
    analyze_GUIs('..\\preprocessed_data\empirical_study\pairs\\results\Layout')
    analyze_GUIs('..\\preprocessed_data\empirical_study\pairs\\results\View')