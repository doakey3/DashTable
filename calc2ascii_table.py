import socket
import uno
import subprocess
from com.sun.star.beans import PropertyValue
from dashtable import html2rst
import sys
import os

# This is a macro for libreoffice calc
# It requires dashtable to work.

"""
Where to put this file
======================

Linux
-----

    /home/<username>/.config/libreoffice/4/user/Scripts/python

Windows
-------
    
    C:/Documents and Settings/<username>/Application Data/OpenOffice.org 2.0/user/Scripts/python

"""

def build_rst(*args):
    document = XSCRIPTCONTEXT.getDocument()

    props_dict = {
        "ReadOnly" : False,
        "FilterName" : "HTML (StarCalc)",
        "FilterOptions":""
        }

    props = []
    for key in props_dict:
        prop = PropertyValue()
        prop.Name = key
        prop.Value = props_dict[key]
        props.append(prop)

    document.storeToURL('file://' + os.getcwd() + '/temp.html', props)

    rst = html2rst(os.getcwd() + '/temp.html', force_headers=True)

    f = open(os.getcwd() + '/.calc2ascii_output.txt', 'w')
    f.write(rst)
    f.close()

    os.remove(os.getcwd() + '/temp.html')

    if sys.platform == "win32":
        subprocess.call(['start', os.getcwd() + '/.calc2ascii_output.txt'])
    else:
        subprocess.call(['xdg-open', os.getcwd() + '/.calc2ascii_output.txt'])


