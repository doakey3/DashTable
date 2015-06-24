""" Program to convert an html file (example: input.html) with a table inside it
    to an ASCII table.
    Caveats: take into consideration the spans: rowspan and columnspan
    modules used: 
    - beautifulsoup: to get the table inside HTML
    - texttable: to convert a list into ascii table
"""

from bs4 import BeautifulSoup
import table2list


# get the table
soup = BeautifulSoup(open('input.html', encoding='utf-8'))
table = soup.find('table')
# convert table to dict with list and rowspan, and colspan
my_dict = table2list.table2list(table)

print(my_dict)