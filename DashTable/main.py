""" Program to convert an html file (example: input.html) with a table inside it
    to an ASCII table.
    Caveats: take into consideration the spans: rowspan and columnspan
    modules used: 
    - beautifulsoup: to get the table inside HTML
    - texttable: to convert a list into ascii table
"""

from bs4 import BeautifulSoup
import dashtable
import html2list


# get the table
datalist, rowspan_list, colspan_list = html2list.html2list("file_path")
#  result = table_list_to_ascii(table, colspan_list, rowspan_list)
result = dashtable.table_list_to_ascii(datalist, rowspan_list, colspan_list)
