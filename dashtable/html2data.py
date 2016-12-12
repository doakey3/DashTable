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
    try:
        rows = table.findAll('tr')
    except AttributeError:
        print("No table found in input text/file")
        quit()

    return len(rows)


def extractTable(html_string):
    """Convert an html string containing a table into data table"""
    data_table = []
    row_count = getRowCount(html_string)
    column_count = getColumnCount(html_string)

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
            ths = rows[r].findAll('th')
            if len(ths) == 0:
                ths = rows[r].findAll('td')
            tds = ths
        else:
            tds = rows[r].findAll('td')

        column = 0
        for i in range(len(tds)):
            data_table[r][column] = tds[i].text.strip()

            if tds[i].has_attr('colspan'):
                column += int(tds[i]['colspan'])
            else:
                column += 1

    return data_table


def extractSpans(html_string):
    """
    Creates a list of the spanned cell groups of [row, column] pairs
    """

    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    rows = table.findAll('tr')
    spans = []
    for r in range(len(rows)):
        if r == 0:
            ths = rows[r].findAll('th')
            if len(ths) == 0:
                ths = rows[r].findAll('td')
            tds = ths
        else:
            tds = rows[r].findAll('td')

        column = 0
        for i in range(len(tds)):
            r_span_count = 1
            c_span_count = 1
            current_column = column

            if tds[i].has_attr('rowspan'):
                r_span_count = int(tds[i]['rowspan'])
            if tds[i].has_attr('colspan'):
                c_span_count = int(tds[i]['colspan'])
                column += c_span_count
            else:
                column += 1

            if r_span_count > 1 or c_span_count > 1:
                new_span = []
                for r_index in range(r, r + r_span_count):
                    for c_index in range(current_column, column):
                        new_span.append([r_index, c_index])
                spans.append(new_span)

    return spans


def headersPresent(html_string):
    """
    checks if the html table contains headers and returns True/False
    """
    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    th = table.findAll('th')
    if len(th) > 0:
        return True
    else:
        return False


if __name__ == '__main__':

    html_string = """
        <table border="solid black">
        <tr>
        <td>aaaa</td>
        <td colspan=2>COLSPAN</td>
        <td rowspan=2>ROWSPAN</td>
        </tr>
        <tr>
        <td>jj</td>
        <td>under_COLSPAN1</td>
        <td>under_COLSPAN2</td>
        </tr>
        <tr>
        <td>fff</td>
        <td>kk</td>
        <td>hhhhh</td>
        <td>iii</td>
        </tr>
        </table>
    """

    table = extractTable(html_string)
    for row in table:
        print(row)

    spans = extractSpans(html_string)
    for span in spans:
        print(span)
