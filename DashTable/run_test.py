from html2rst import html2rst
import os

for file in os.listdir(os.getcwd() + '/../test_files'):
    path = os.getcwd() + '/../test_files/' + file
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    string = ''.join(lines)
    print(file)
    print(html2rst(string))
