from bs4 import BeautifulSoup


def getColumnCount(html_string):
    """returns the number of columns in the html table"""

    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    if not table:
        return 0
        
    column_counts = []
    rows = table.findAll('tr')
    if len(rows) == 0:
        return 0
        
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
    if not table:
        return 0

    row_count = 0
        
    column_counts = []
    rows = table.findAll('tr')
    if len(rows) == 0:
        return 0

    r = 0
    while r < len(rows):
        row_add = 1
        if r == 0:
            columns = rows[r].findAll('th')
            if len(columns) == 0:
                columns = rows[r].findAll('td')
        else:
            columns = rows[r].findAll('td')

        if len(columns) == 0:
            return 1

        else:
            if columns[0].has_attr('rowspan'):
                row_add = int(columns[0]['rowspan'])

        row_count += row_add
        r += row_add

    return row_count
            
def convertRichText(html_string):
    """Fix the newlines, bolds, italics"""
    
    html_string = html_string.replace('<br>', '<br>\n')
    html_string = html_string.replace('<p>', '<p>\n')
    html_string = html_string.replace('<b>', '**')
    html_string = html_string.replace('<\b>', '**')
    html_string = html_string.replace('<i>', '*')
    html_string = html_string.replace('</i>', '*')

    return html_string

def findUnassignedCell(table):
    """
    Search through table and return the first [row, column] pair of a
    cell whose value == None
    """
    for row in range(len(table)):
        for column in range(len(table[row])):
            if table[row][column] == None:
                return row, column

def extractTable(html_string):
    """Convert an html string containing a table into data table"""
    data_table = []
    row_count = getRowCount(html_string)
    column_count = getColumnCount(html_string)

    for r in range(row_count):
        data_table.append([])
        for c in range(column_count):
            data_table[r].append(None)

    html_string = convertRichText(html_string)
    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    if not table:
        return ''

    trs = table.findAll('tr')
    if len(trs) == 0:
        return [['']]

    for tr in range(len(trs)):
        if tr == 0:
            ths = trs[tr].findAll('th')
            if len(ths) == 0:
                ths = trs[tr].findAll('td')
            tds = ths
        else:
            tds = trs[tr].findAll('td')
        
        for i in range(len(tds)):
            row, column = findUnassignedCell(data_table)
            span_column_count = 1
            span_row_count = 1
            
            if tds[i].has_attr('colspan'):
                span_column_count = int(tds[i]['colspan'])
            if tds[i].has_attr('rowspan'):
                span_row_count = int(tds[i]['rowspan'])

            for row_prime in range(row, row + span_row_count):
                for column_prime in range(column, column + span_column_count):
                    if row_prime == row and column_prime == column:
                        data_table[row_prime][column_prime] = tds[i].text.strip()
                    else:
                        data_table[row_prime][column_prime] = ""

    return data_table


def extractSpans(html_string):
    """
    Creates a list of the spanned cell groups of [row, column] pairs
    """

    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    if not table:
        return []
        
    rows = table.findAll('tr')
    if len(rows) == 0:
        return []
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
    if not table:
        return False
        
    th = table.findAll('th')
    if len(th) > 0:
        return True
    else:
        return False

def html2data(html_string):
    table_data = extractTable(html_string)
    spans = extractSpans(html_string)
    use_headers = headersPresent(html_string)

    return table_data, spans, use_headers


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
