DashTable
=========
HTML table to ASCII table, colspan & Rowspan allowed!

## What is this package used for?

There are some ASCII table creator out there.
For those who don't know, an ASCII table is like:

```
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
```

But, for all these programs, I didn't find any **rowspan** or **colspan** integration! (If you look on the 3rd row, second column, you can see that the column spans 3 other columns. That's a `Colspan=3`).

So, I decide to create it myself!

(Maybe you're asking what the point of ASCII table? The thing is, it's useful for example for ReST formatting ( http://docutils.sourceforge.net/docs/user/rst/quickref.html#tables ).
Basically, you can give to certain programs Rest-formatted tables (i.e ASCII table) and voilà: superb formating to be displayed)

ReST is perfect formatting, a bit like the formatting you can get with the browser, but without need of it, and especially, no need of:
```
  <tr>
  <td>Jack</td>
  <td colspan=2 rowspan=2>Undisclosed</td>
  <td>graphist</td>
  </tr>
```
which is difficult to read usually...


## Installation

This package needs only one depency: Beautisoup4. It's a scaper (it extracts useful data from html file: here, it extracts cells from HTML table): http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
```
pip install beautifulsoup4
```
then, you can download the source here, or using pip:
`pip install DashTable`

## Using it:

It uses as input an html file whith a table inside (in HTML format of course)
then:

```python
from DashTable.main import main

myfile = "path/to/your/file.html"
print(main(myfile))
```

## Test Files:

there are into test_files folder:

```python
from DashTable.main import main
print(main('test_files/simple_input.html')  # a simple html table
print(main('test_files/colspan_input.html')  # a html table with colspan cells
print(main('test_files/rowspan_input.html')  # a html table with rowspan cells
print(main('test_files/colspanANDrowspan_input.html')  # Rowspan AND colspan, both of them!
```

The `main` module does all the work: see below.
If you want, you can use only the html2list module (and return so only the 3 lists described below, or only the dashTable module.

# Inner working:
The `main` module calls the `html2llist` module, than the `dashTable` module:

* the `html2list` module :
It extract the raw data from the table and the specific rowspan and colspan of each cell.
it returns 3 lists: one with the data and the 2 others describing the colspan and rowspan cells.

for ex.:
```
  <tr>
  <td>Jack</td>
  <td colspan=2 rowspan=2>Undisclosed</td>
  <td>graphist</td>
  </tr>
```
will be converted to: 
```python
data_list = ['Jack','Undisclosed','', 'graphist'] 
rowspan_list = [0, 0, 0, 0] #no colspan, basically
colspan_list = [0, 1, 1, 0]
 ``` 

* the `dashTable` module :
Give it these 3 data lists and a string (the ASCII table) is returned.


## Contributors

If you have some suggestions, critics, problems to make it work in your special configuration, I can (or try..) help!

## License

LGPL