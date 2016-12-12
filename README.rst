.. contents::

Convert HTML tables to ASCII tables; colspan & rowspan allowed!

Introduction
============

Here is an ASCII table example:

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

dashtable supports colspan and rowspan. It takes html code like this:

.. code-block:: html

    <tr>
    <td>Jack</td>
    <td colspan=2 rowspan=2>Undisclosed</td>
    <td>graphist</td>
    </tr>

And converts it to an easy-to-read table.

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

Example:

.. code-block:: python

    from dashtable import html2rst

    filepath = "path/to/html/file.html"
    print(html2rst(filepath, force_headers=False))

You may use a filepath or a string as the input for the function. If you
have an html table that does not have headers (<td> instead of <th> on
the first row), but you want your ASCII table to use headers, you can
set the optional parameter "force_headers" to True.

html2rst can also be used from the command line like this:

::

    python html2rst.py input.html output.rst --force_headers

The "--force_headers" is optional.
