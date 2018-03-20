=========
DashTable
=========
dashtable has functions for converting data to reStructuredText
tables and Markdown tables, as well as methods for generating data from
these text-tables. It can quickly convert html tables to rst, but you
may have better results with pandoc.

Methods
=======
:html2rst:       Convert html table to `RST grid table`_
:html2md:        Convert html table to Markdown table
:data2md:        Convert a list of lists of strings to Markdown Table
:data2rst:       Convert a list of lists of strings to `RST grid Table`_
:data2simplerst: Convert a list of lists of strings to a `simple RST
                 Table`_
:grid2data:      Convert an `RST grid table`_ to data
:simple2data:    Convert a `simple RST table`_ to data

.. _RST grid table: http://docutils.sourceforge.net/docs/user/rst/quickref.html#tables
.. _simple RST Table: http://docutils.sourceforge.net/docs/user/rst/quickref.html#tables

Installation
============
dashtable can be installed using pip::

    sudo pip install dashtable

Depending on how you'd like to use dashtable, you may need to install
some dependencies.

Dependencies
============
Several of the functions in dashtable have no outside requirements.
However, for the following functions you will need to install certain
dependencies:

:html2rst: BeautifulSoup_,
:html2md: BeautifulSoup_
:html2data: BeautifulSoup_,
:grid2data: docutils_
:simple2data: docutils_

.. _docutils: http://docutils.sourceforge.net/
.. _pandoc: https://pandoc.org/
.. _BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/

Usage
-----
Complete documentation on usage can be found on `Read the Docs`_.

.. _Read the Docs: http://dashtable.readthedocs.io/en/latest/Code.html
