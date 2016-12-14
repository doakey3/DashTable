# This is a macro for libreoffice calc
# It will saveAs html, convert html to rst, then open rst in text editor
# The html file is destroyed after conversion
# the rst remains as .ascii_table.txt in the home folder

"""
Where to put this file
======================

Linux
-----

  /home/<username>/.config/libreoffice/4/user/Scripts/python

Windows
-------

  C:/Program Files (x86)/LibreOffice 5/share/Scripts/python

  Then put bs4 and dashtable in:

  C:/Program Files (x86)/LibreOffice 5/program/python-core-3.3.0/lib/site-packages

"""

import subprocess
from dashtable import html2rst, html2md
import sys
import os

def build_rst(doc=None):
    from com.sun.star.beans import PropertyValue
    
    if not doc:
        document = XSCRIPTCONTEXT.getDocument()
    else:
        document = doc

    html_url = os.path.join(os.path.expanduser('~'), 'temp.html')
    html_url = html_url.replace('\\', '/')

    if not html_url.startswith('/'):
        save_url = 'file:///' + html_url
    else:
        save_url = 'file://' + html_url

    props = [PropertyValue(Name='FilterName', Value='HTML (StarCalc)')]

    document.storeToURL(save_url, props)

    rst = html2rst(html_url, force_headers=True)

    rst_url = os.path.join(os.path.expanduser('~'), '.ascii_table.txt')
    rst_url = rst_url.replace('\\', '/')

    f = open(rst_url, 'w')
    f.write(rst)
    f.close()

    os.remove(html_url)

    if sys.platform == "win32":
        subprocess.call(['start',"", rst_url], shell=True)
    else:
        subprocess.call(['xdg-open', rst_url])

def build_md(doc=None):
    from com.sun.star.beans import PropertyValue
    
    if not doc:
        document = XSCRIPTCONTEXT.getDocument()
    else:
        document = doc

    html_url = os.path.join(os.path.expanduser('~'), 'temp.html')
    html_url = html_url.replace('\\', '/')

    if not html_url.startswith('/'):
        save_url = 'file:///' + html_url
    else:
        save_url = 'file://' + html_url

    props = [PropertyValue(Name='FilterName', Value='HTML (StarCalc)')]

    document.storeToURL(save_url, props)

    md = html2md(html_url)

    md_url = os.path.join(os.path.expanduser('~'), '.ascii_table.txt')
    md_url = md_url.replace('\\', '/')

    f = open(md_url, 'w')
    f.write(md)
    f.close()

    os.remove(html_url)

    if sys.platform == "win32":
        subprocess.call(['start',"", md_url], shell=True)
    else:
        subprocess.call(['xdg-open', md_url])

if __name__ == '__main__':
    """
    To run this macro from outside calc, start calc with this first:

soffice --calc \
--accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
    """
    
    import socket
    import uno

    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext(
				"com.sun.star.bridge.UnoUrlResolver", localContext )
    ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
    document = desktop.getCurrentComponent()
    build_rst(doc=document)
    #build_md(doc=document)
