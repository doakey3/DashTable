About
=====
When it comes to converting html to rst, pandoc_ does an excellent
job... except for tables. dashtable is designed to fill this gap by
creating a way to convert html tables into reStructuredText or Markdown.

dashtable also has functions for converting data to reStructuredText
tables and Markdown tables, as well as methods for generating data from
these text-tables.

Methods
-------
:html2rst:       Convert html table to `RST grid table`_
:html2md:        Convert html table to Markdown table
:data2md:        Convert a list of lists of strings to Markdown Table
:data2rst:       Convert a list of lists of strings to `RST grid Table`_
:data2md:        Convert a list of lists of strings to a Markdown Table
:data2simplerst: Convert a list of lists of strings to a `simple RST
                 Table`_
:grid2data:      Convert an `RST grid table`_ to data
:simple2data:    Convert a `simple RST table`_ to data

.. _pandoc: https://pandoc.org/
.. _RST grid table: http://docutils.sourceforge.net/docs/user/rst/quickref.html#tables
.. _simple RST Table: http://docutils.sourceforge.net/docs/user/rst/quickref.html#tables
