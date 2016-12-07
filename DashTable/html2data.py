from bs4 import BeautifulSoup

def getColumnCount(html_string):
    """returns the number of columns in the html table"""

    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    column_counts = []
    rows = table.findAll('tr')

    for r in range(len(rows)):
        if r == 0:
            columns = rows[r].findAll('th')
            if len(columns) == 0:
                columns = rows[r].findAll('td')
        else:
            columns = rows[r].findAll('td')

        count = 0
        for c in range(len(columns)):
            if columns[c].has_attr('colspan'):
                count = int(columns[c]['colspan'])
            else:
                count += 1
                
        column_counts.append(count)

    return max(column_counts)


def getRowCount(html_string):
    """returns the number of rows in the html table"""

    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    rows = table.findAll('tr')

    return len(rows)


def html2list(html_string):
    """Convert an html string containing a table into data table"""
    data_table = []
    column_count = getColumnCount(html_string)
    row_count = getRowCount(html_string)

    for r in range(row_count):
        data_table.append([])
        for c in range(column_count):
            data_table[r].append('')

    html_string = html_string.replace('<br>', '<br>\n')
    html_string = html_string.replace('<p>', '<p>\n')

    soup = BeautifulSoup(html_string, 'html.parser')

    table = soup.find('table')
    rows = table.findAll('tr')

    for b in table.find_all('b'):
        b.replace_with('**' + b.text + '**')

    for i in table.find_all('i'):
        i.replace_with('*' + i.text + '*')

    for r in range(len(rows)):
        if r == 0:
            columns = rows[r].findAll('th')
            if len(columns) == 0:
                columns = rows[r].findAll('td')
        else:
            columns = rows[r].findAll('td')

        for c in range(len(columns)):
            data_table[r][c] = columns[c].text.strip()

    return data_table

def collectSpans(html_string):
    """Creates a list of the spanned cell groups"""
    pass
    
if __name__ == '__main__':
    f = open('/home/doakey/Desktop/test.html', 'r')
    lines = f.readlines()
    f.close()

    html_string = ''.join(lines)
    table = html2list(html_string)
    for r in range(len(table)):
        print(table[r])
