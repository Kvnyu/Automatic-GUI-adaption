import os
import shutil
def check_results(result_path, apk_path):
    keyword = 'events'
    for root, dirs, files in os.walk(result_path):
        for dir in dirs:
            print(dir)
            full_dir = os.path.join(root, dir)
            for root2, dirs2, files2 in os.walk(full_dir):
                for dir2 in dirs2:
                    if dir2 == 'coresponding_snapshots_dir' or dir2 == 'main_activity':
                        continue
                    is_success = False
                    full_dir2 = os.path.join(root2, dir2)
                    for root3, dirs3, files3 in os.walk(full_dir2):
                        if keyword in dirs3:
                            is_success = True
                    if is_success:
                        sucess_apk = os.path.join(apk_path, dir, dir2)
                        try:
                            os.remove(sucess_apk)
                        except FileNotFoundError:
                            print('file has been removed')
                    else:
                        failure_dir = os.path.join(result_path, dir, dir2)
                        try:
                            shutil.rmtree(failure_dir)
                        except FileNotFoundError:
                            print('dir has been removed')
                    is_success = False


if __name__=='__main__':
    check_results('results\high_similarity_apps', 'high_similarity_apps')