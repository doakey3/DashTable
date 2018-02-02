import os
import shutil
import subprocess

shutil.rmtree(os.path.join(os.path.join(os.path.abspath('.'), '_build')))
subprocess.call(['make', 'html'])
