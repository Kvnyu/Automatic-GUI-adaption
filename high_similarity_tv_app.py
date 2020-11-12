import os
import difflib
import shutil

target_dir = './high_similarity_apps'
tv_corresponding_apps_path = 'tv_corresponding_apps.txt'
spacer = '     |||     '
cmd_instructions = []
cmd_instructions.append('droidbot -keep_env -is_emulator ')
cmd_instructions.append('-timeout 30 ')

def check_tv_dic(path):
    file = open(path, 'r')
    similarity = 0
    paths = []
    for line in file.readlines():
        line = line.split(spacer)
        tv_name = line[0]
        an_name = line[1]
        path = line[2]

        tv_name = tv_name.replace("tv", "")
        tv_name = tv_name.replace("TV", "")
        tv_name = tv_name.replace("HD", "")

        an_name = an_name.replace("HD", "")

        similarity = difflib.SequenceMatcher(None, tv_name, an_name).quick_ratio()
        if similarity > 0.9:
            #print(line[0]+" "+line[1])
            if not path in paths:
                paths.append(path)
            else:
                print('path:'+path+'have been in paths')

    return paths

def cmd_evoker(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for file_path in files:
            apk_path = root+'/'+file_path
            print(apk_path)
            cmd_instructions.append('-a '+apk_path+' ')
            save_path = 'results'+'/' +file_path
            print(save_path)
            cmd_instructions.append('-o '+save_path)
            cmd = "".join(cmd_instructions)
            os.system(cmd)

def move_file(path):
    dir = path[path.rindex('/'):]
    shutil.copytree(path, target_dir+dir)

if __name__ == '__main__':
    paths = check_tv_dic(tv_corresponding_apps_path)
    print(len(paths))
    for path in paths:
        print(path[:-1])
        move_file(path[:-1])
        #cmd_evoker(path[:-1])