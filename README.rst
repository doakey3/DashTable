This package was originally written by gustavklopp_

.. _gustavklopp: https://github.com/gustavklopp

.. contents::

Introduction
============

DashTable takes codified tables like this html table:

.. code-block:: html

    <table>
    <tr>
        <th>Header 1</th>
        <th>Header 2</th>
        <th>Header 3</th>
    </tr>
    <tr>
        <td>body row 1</td>
        <td>column 2</td>
        <td>column 3</td>
    </tr>
    <tr>
        <td>body row 2</td>
        <td colspan=2>Cells may span columns</td>
    </tr>
    <tr>
        <td>body row 3</td>
        <td rowspan=2>Cells may span rows.</td>
        <td rowspan=2>- Cells<br>- contain<br>- blocks</td>
    </tr>
    <tr>
        <td>body row 4</td>
    </tr>
    </table>

And converts it to an easy-to-read table like this:

::

    +------------+------------+-----------+
    | Header 1   | Header 2   | Header 3  |
    +============+============+===========+
    | body row 1 | column 2   | column 3  |
    +------------+------------+-----------+
    | body row 2 | Cells may span columns.|
    +------------+------------+-----------+
    | body row 3 | Cells may  | - Cells   |
    +------------+ span rows. | - contain |
    | body row 4 |            | - blocks. |
    +------------+------------+-----------+

There are many ASCII table creators, but most do not support column
spanning and row spanning like you see in the table above. The table
above is based on the reStructured_ table format.

.. _reStructured: http://docutils.sourceforge.net/rst.html

Installation
============

This package requires `Beautiful Soup 4`_ which will install alongside
dashtable if you don't already have it.

.. _Beautiful Soup 4: https://www.crummy.com/software/BeautifulSoup/

To install dashtable, use pip

::

    pip install dashtable

Usage
=====

reStructured Tables
-------------------

.. code-block:: python

    from dashtable import html2rst

    filepath = "path/to/html/file.html"
    print(html2rst(filepath, force_headers=False))

You may use a filepath or a string as the input for the function.

You may force the output table's first row to be a header row even if
the input html's first row is not. To do this, set the  force_headers
parameter to True.

Command line method:

::

    python html2rst.py input.html output.rst --force_headers

The "--force_headers" is optional.

Markdown Tables
---------------

Convert html tables to the markdown_ format.

_markdown: 

.. code-block:: python

    from dashtable import html2md

    filepath = "path/to/html/file.html"
    print(html2md(filepath))

Command line method:

::

    python html2md.py input.html output.md

LibreOffice Calc Macro
======================

The file "calc2ascii_table" is a macro for LibreOffice Calc to create
ascii tables from inside Calc.

Installation Linux
------------------

Install dashtable with pip, then put calc2ascii_table.py into this
directory:

::

    /home/<username>/.config/libreoffice/4/user/Scripts/python

If there is no Scripts folder, then make one. You can now run the macro
from within calc.

Installation Windows
--------------------

Download dashtable and bs4. Put these into the site-packages folder
inside LibreOffice's python. Then place calc2ascii_table in this
directory:

::

    C:/Program Files (x86)/LibreOffice 5/share/Scripts/python

    
