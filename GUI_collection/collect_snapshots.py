import os
import shutil

def copy_snapshot_json(name, dst, src, new_name=None):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for root, dirs, files in os.walk(src, topdown=False):
        for file in files:
            if name in file:
                #print('copy file'+file)
                if new_name != None:
                    shutil.copy(os.path.join(src, file), os.path.join(dst, new_name + "_" + file))
                else:
                    shutil.copy(os.path.join(src, file), os.path.join(dst, file))


def copy_snapshot_json_skeleton(name, dst, src, new_name=None):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for root, dirs, files in os.walk(src, topdown=False):
        for file in files:
            if 'screen' in file:
                file_new = file.replace('screen', 'state')
            if name in file_new:
                #print('copy file'+file)
                if new_name != None:
                    shutil.copy(os.path.join(src, file), os.path.join(dst, new_name + "_" + file))
                else:
                    shutil.copy(os.path.join(src, file), os.path.join(dst, file))

def check_main_activity(activity_name):
    dic = ['home', 'Home', 'Main', 'main', 'Welcome', 'welcome']
    for word in dic:
        if word in activity_name:
            return True
    return False


def check_an_tv_result(path):
    status = False
    count = 0
    keyword = 'events'
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            full_dir = os.path.join(root, dir)
            for root2, dirs2, files2 in os.walk(full_dir):
                if keyword in dirs2:
                        count += 1
                        break

    if count >= 2:
        status = True
    return status

