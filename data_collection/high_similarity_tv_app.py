import os
import difflib
import shutil

target_dir = 'high_similarity_apps'
tv_corresponding_apps_path = 'tv_corresponding_apps.txt'
spacer = '     |||     '

def check_tv_dic(path):
    file = open(path, 'r')
    similarity = 0
    paths = []
    for line in file.readlines():
        line = line.split(spacer)
        tv_name = line[0]
        an_name = line[1]
        path = line[2]
        similarity = calculate_similarity(tv_name, an_name)
        if similarity > 0.9:
            #print(line[0]+" "+line[1])
            if not path in paths:
                paths.append(path)
            #else:
                #print('path:'+path+'have been in paths')
    return paths


def move_file(path):
    dir = path[path.rindex('/')+1:]
    find_high_similarity_apks(dir, path)
    #shutil.copytree(path, target_dir+dir)

def find_high_similarity_apks(ref, path):
    for root, dirs, apks in os.walk(path):
        for apk in apks:
            similarity = calculate_similarity(ref, apk)
            print('similarity:'+str(similarity))
            if similarity > 0.9:
                print('high similarity: '+apk+' '+ref)
                src_file = os.path.join(root, apk)
                dst_dir = os.path.join(target_dir, ref)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                dst_file = os.path.join(dst_dir, apk)
                shutil.copy(src_file, dst_file)


def remove_low_similarity_apks(target_dir):
    for root, dirs, files in os.walk(target_dir):
        for dir in dirs:
            path = os.path.join(root, dir)
            for root_2, dirs_2, apks in os.walk(path):
                for apk in apks:
                    similarity = calculate_similarity(dir, apk)
                    print('similarity:'+str(similarity))
                    if similarity<0.9:
                        print(apk+' '+dir)
                        remove_file = os.path.join(root_2, apk)
                        if os.path.exists(remove_file):
                            os.remove(remove_file)


def calculate_similarity(dir, apk):
    apk = apk.replace("tv_", "")
    apk = apk.replace("TV", "")
    apk = apk.replace("HD", "")
    apk = apk.replace(".apk", "")

    dir = dir.replace("HD", "")
    dir = dir.replace("tv", "")
    dir = dir.replace("TV", "")
    similarity = difflib.SequenceMatcher(None, dir, apk).quick_ratio()
    return similarity


if __name__ == '__main__':
    paths = check_tv_dic(tv_corresponding_apps_path)
    print(len(paths))
    for path in paths:
        print(path[:-1])
        move_file(path[:-1])
    remove_low_similarity_apks(target_dir)