import os

#apks/category/app name directory/andorid.apk + tv.apk. Example: test_apks/video_player/Youtube/youtube.apk + tv_youtube.tv
h_apps_dir = 'test_apks'
save_dir = 'test_results'

def cmd_evoker(path):
    for root, dirs, files in os.walk(path, topdown=True):
        for file_path in files:
            cmd_instructions = []
            cmd_instructions.append('droidbot ')
            #cmd_instructions.append('-is_emulator ')
            cmd_instructions.append('-keep_env ')
            cmd_instructions.append('-grant_perm ')
            cmd_instructions.append('-ignore_ad ')
            cmd_instructions.append('-timeout 1200 ')
            cmd_instructions.append('-policy bfs_greedy ')
            apk_path = os.path.join(root, file_path)
            print(apk_path)
            cmd_instructions.append('-a '+apk_path+' ')
            save_path_dir = os.path.join(save_dir, root)
            if not os.path.exists(save_path_dir):
                os.makedirs(save_path_dir)
            save_path = os.path.join(save_path_dir, file_path)
            print(save_path)
            cmd_instructions.append('-o '+save_path)
            cmd = "".join(cmd_instructions)
            os.system(cmd)


if __name__=='__main__':
    for root, dirs, files in os.walk(h_apps_dir, topdown=True):
        print(len(dirs))
        for dir in dirs:
            print(dir)
            path = os.path.join(root, dir)
            cmd_evoker(path)