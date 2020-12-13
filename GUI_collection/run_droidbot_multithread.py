#coding = utf-8
import threading
import os

input_path1 = 'high_similarity_apps/1'
input_path2 = 'high_similarity_apps/2'
input_path3 = 'high_similarity_apps/3'

output_path1 = '..\preprocessed_data'
output_path2 = '..\preprocessed_data'
output_path3 = '..\preprocessed_data'

emulator1 = 'emulator-5554'
emulator2 = 'emulator-5556'
emulator3 = 'emulator-5558'

class Droidbot_Thread (threading.Thread):
    def __init__(self, thread_id, name, input_path, output_path, emulator):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.input_path = input_path
        self.output_path = output_path
        self.emulator = emulator

    def run(self):
        print('start ' + self.name)
        for root, dirs, files in os.walk(self.input_path, topdown=True):
            print(len(dirs))
            for dir in dirs:
                print(dir)
                path = os.path.join(root, dir)
                cmd_evoker(path, self.output_path, self.emulator)
        print('exit ' + self.name)


def cmd_evoker(input_path, output_path, emulator):
    save_dir = output_path
    for root, dirs, files in os.walk(input_path, topdown=True):
        for file_path in files:
            cmd_instructions = []
            cmd_instructions.append('droidbot ')
            cmd_instructions.append('-is_emulator ')
            cmd_instructions.append('-d ' + emulator + ' ')
            cmd_instructions.append('-keep_env ')
            cmd_instructions.append('-grant_perm ')
            cmd_instructions.append('-ignore_ad ')
            cmd_instructions.append('-timeout 600 ')
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


if __name__ == '__main__':
    thread1 = Droidbot_Thread(1, "Thread-1", input_path1, output_path1, emulator1)
    thread2 = Droidbot_Thread(2, "Thread-2", input_path2, output_path2, emulator2)
    thread3 = Droidbot_Thread(3, "Thread-3", input_path3, output_path3, emulator3)

    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
    print("exit main thread")