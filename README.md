DashTable
=========
HTML table to ASCII table, colspan & Rowspan allowed!
-----------------------------------------------------

## What this package is used for?

There are some ASCII table creator out there.
For those who don't know, an ASCII table is like:

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

But, for all of them, I didn't find any rowspan or colspan integration! (If you look on the 3rd row, second column, you can see that the column spans 3 other columns. That's a Colspan=3).

So, I decide to create it myself!

(Maybe you're asking what the point of ASCII table? The thing is, it's useful for example for ReST formatting ( http://docutils.sourceforge.net/docs/user/rst/quickref.html#tables ).
Basically, you can give to certain programs Rest-formatted tables (i.e ASCII table) and voilà: superb formating to be displayed)


## Installation

This package needs only one depency: Beautisoup4. It's a scaper (it extracts useful data from html file: here, it extracts cells from HTML table): http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
*pip install beautifulsoup4*

## Using it:

It uses as input an html file whith a table inside (in HTML format of course)
then:

import DashTable

myfile = "path/to/your/file.html"
print(DashTable.main(myfile)

# Inner working:
there's an 'html2list.py' module which extract the raw data from the table and the specific rowspan and colspan of each cell.
Then, the magic is done thanks to the dashtable.py! Give it these 3 data lists and a string (the ASCII table) is returned.

## Contributors

If you have some suggestions, critics, problems to make it work in your special configuration, I can (or try..) help!

## License

LGPL