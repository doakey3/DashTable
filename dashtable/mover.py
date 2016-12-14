import os
import shutil

lib_path = "/usr/lib/python3.5/site-packages/dashtable/"
home_path = "/home/doakey/Sync/Programming/DashTable/dashtable/"

for file in os.listdir(lib_path):
    if not file == '__pycache__':
        os.remove(os.path.join(lib_path, file))

for file in os.listdir(home_path):
    if not file == 'mover.py' and not file == '__pycache__':
        f_path = os.path.join(home_path, file)
        shutil.copy(f_path, os.path.join(lib_path, file))
