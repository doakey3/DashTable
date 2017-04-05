from dashtable import html2rst, html2md
import subprocess
import os

for file in os.listdir(os.getcwd() + '/test_files'):
    if file.endswith('.html'):
        path = os.path.join(os.getcwd(), 'test_files', file)
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        
        string = ''.join(lines)
        
        print(file)
        print(html2rst(string))
        print('\n')
        print(html2md(string))
        print('\n')

        script = os.path.join(os.getcwd(), 'dashtable/html2rst.py')
        filename = os.path.splitext(file)[0]
        outfile = os.path.join(os.getcwd(), 'test_files', filename + '.txt')
        subprocess.call(['python', script, path, outfile])
