import os

files = []
included = []
for file in sorted(os.listdir(os.getcwd())):
    if file.endswith('.py') and not file in ['_make_init.py', '__init__.py']:

        fname = os.path.splitext(file)[0]
        included.append(fname)
        files.append('from .' + fname + ' import ' + fname)

f = open('__init__.py', 'w')

#all_string = '__all__ = [\n'
#for item in included:
#    all_string += '    "' + item + '",\n'
#all_string += ']'

imports = '\n'.join(files)

#f.write(all_string + '\n\n' + imports)
f.write(imports)
f.close()
