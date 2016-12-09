=========
DashTable
=========

Convert HTML tables to ASCII tables; colspan & rowspan allowed!

Introduction
============

For those who don't know, an ascii table looks like this:

::

    +------------------------+------------+----------+----------+
    | Header row, column 1   | Header 2   | Header 3 | Header 4 |
    | (header rows optional) |            |          |          |
    +========================+============+==========+==========+
    | body row 1, column 1   | column 2   | column 3 | column 4 |
    +------------------------+------------+----------+----------+
    | body row 2             | Cells may span columns.          |
    +------------------------+------------+---------------------+
    | body row 3             | Cells may  | - Table cells       |
    +------------------------+ span rows. | - contain           |
    | body row 4             |            | - body elements.    |
    +------------------------+------------+---------------------+

There are many ASCII table creators, but I could not find any that
support **rowspan** or **colspan**! (on the 3rd row, second column, you
can see that the column spans 3 other columns. That's a "colspan=3").

DashTable supports colspan and rowspan. It takes html code like this:

.. code-block:: html

    <tr>
    <td>Jack</td>
    <td colspan=2 rowspan=2>Undisclosed</td>
    <td>graphist</td>
    </tr>

And converts it to an easy-to-read table.

Installation
============

This package requires `Beautiful Soup 4`_ which can be installed with
pip. Like this:

.. code-block:: python

    pip install bs4

.. _Beautiful Soup 4: https://www.crummy.com/software/BeautifulSoup/

Next, install DashTable by downloading it, changing directory to the
DashTable folder and running this command:

.. code-block::

    python setup.py install

Usage
=====

The important function in DashTable is html2rst. Here is a usage
example:

.. code-block:: python

    from DashTable import html2rst

    filepath = "path/to/html/file.html"
    print(html2rst(filepath, force_headers=False))

You may use a filepath or a string as the input for the function. If you
have an html table that does not have headers (<td> instead of <th> on
the first row), but you want your ASCII table to use headers, you can
set the "force_headers" option to true.

html2rst can also be used from the command line like this:

..code-block::

    python html2rst.py input.html output.rst


Licence
-------

GNU General Public License
