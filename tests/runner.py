import os
import sys

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(file_path))

import dashtable

path = os.path.join(os.getcwd(), 'static')

for file in os.listdir(path):
    if file.endswith('.html'):
        text = open(os.path.join(path, file), 'r', encoding='UTF-8').read()
        data, spans, use_headers = dashtable.html2data(text)
        if not data == '':
            table = dashtable.data2rst(data, spans, use_headers=True, center_headers=True, center_cells=True)
            try:
                print(table)
            except UnicodeEncodeError:

                print(table.encode('utf-8'))