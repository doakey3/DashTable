from dashtable import html2rst

filepath = 'table.html'
text = html2rst(filepath, force_headers=True)
f = open('/home/doakey/Desktop/test.txt', 'w')
f.write(text)
f.close()
