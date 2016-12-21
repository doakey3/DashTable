from bs4.element import Tag
from bs4 import BeautifulSoup

try:
    from .dashutils import getSpanRowCount, sortSpans, getSpan

except SystemError:
    from dashutils import getSpanRowCount, sortSpans, getSpan


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
            if table[row][column] is None:
                return row, column
    return row, column


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


def getColumnCount(html_string):
    """returns the number of columns in the html table"""

    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    if not table:
        return 0

    column_counts = []
    trs = table.findAll('tr')
    if len(trs) == 0:
        return 0

    for tr in range(len(trs)):
        if tr == 0:
            tds = trs[tr].findAll('th')
            if len(tds) == 0:
                tds = trs[tr].findAll('td')
        else:
            tds = trs[tr].findAll('td')

        count = 0
        for td in tds:
            if td.has_attr('colspan'):
                count += int(td['colspan'])
            else:
                count += 1

        column_counts.append(count)

    return max(column_counts)


def getRowCount(spans):
    """Get the number of rows"""

    if spans == []:
        return 0
    row_counts = {}
    spans = sortSpans(spans)
    for span in spans:
        try:
            row_counts[str(span[0][1])] += getSpanRowCount(span)
        except KeyError:
            row_counts[str(span[0][1])] = getSpanRowCount(span)

    values = list(row_counts.values())
    return max(values)


def extractSpans(html_string):
    """
    Creates a list of the spanned cell groups of [row, column] pairs
    """

    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    if not table:
        return []

    trs = table.findAll('tr')
    if len(trs) == 0:
        return []

    spans = []
    for tr in range(len(trs)):
        if tr == 0:
            ths = trs[tr].findAll('th')
            if len(ths) == 0:
                ths = trs[tr].findAll('td')
            tds = ths
        else:
            tds = trs[tr].findAll('td')

        column = 0
        for td in tds:
            r_span_count = 1
            c_span_count = 1
            current_column = column

            if td.has_attr('rowspan'):
                r_span_count = int(td['rowspan'])
            if td.has_attr('colspan'):
                c_span_count = int(td['colspan'])
                column += c_span_count
            else:
                column += 1

            new_span = []
            for r_index in range(tr, tr + r_span_count):
                for c_index in range(current_column, column):
                    if not getSpan(spans, r_index, c_index):
                        new_span.append([r_index, c_index])

            if len(new_span) > 0:
                spans.append(new_span)

    return spans


def extractTable(html_string, row_count, column_count):
    """Convert an html string to data table"""
    html_string = convertRichText(html_string)

    data_table = []
    for row in range(0, row_count):
        data_table.append([])
        for column in range(0, column_count):
            data_table[-1].append(None)

    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')

    if not table:
        return ''

    trs = table.findAll('tr')
    if len(trs) == 0:
        return [['']]

    for tr in range(len(trs)):
        ths = trs[tr].findAll('th')
        if len(ths) == 0:
            tds = trs[tr].findAll('td')
        else:
            tds = ths

        if len(tds) == 0:
            tds = []
            for i in range(0, column_count):
                tds.append(Tag("", name=""))

        for i in range(len(tds)):
            td = tds[i]
            row, column = findUnassignedCell(data_table)

            r_span_count = 1
            c_span_count = 1

            if td.has_attr('rowspan'):
                r_span_count = int(td['rowspan'])
            if td.has_attr('colspan'):
                c_span_count = int(td['colspan'])

            for row_prime in range(row, row + r_span_count):
                for column_prime in range(column, column + c_span_count):
                    if row_prime == row and column_prime == column:
                        text = td.text.strip()
                        data_table[row_prime][column_prime] = text
                    else:
                        data_table[row_prime][column_prime] = ""

            if i + 1 < column_count and i == len(tds) - 1:
                for x in range(len(tds), column_count):
                    if data_table[row][x] is None:
                        data_table[row][x] = ""
    for row in range(len(data_table)):
        for column in range(len(data_table[row])):
            if not data_table[row][column]:
                data_table[row][column] = ""

    return data_table


def html2data(html_string):
    spans = extractSpans(html_string)
    column_count = getColumnCount(html_string)
    row_count = getRowCount(spans)

    count = 0
    while count < len(spans):
        if len(spans[count]) == 1:
            spans.pop(count)
        else:
            count += 1

    table = extractTable(html_string, row_count, column_count)

    use_headers = headersPresent(html_string)

    return table, spans, use_headers

if __name__ == '__main__':

    html_string = """
<table cellspacing="0" border="0">
	<colgroup width="193"></colgroup>
	<colgroup width="374"></colgroup>
	<tr>
		<td colspan=2 height="17" align="left"><font face="DejaVu Sans Mono">--------------------------------------------------------------------</font></td>
		</tr>
	<tr>
		<td height="47" align="left"><font face="DejaVu Sans Mono">Abdominal Pain Diff Dx</font></td>
		<td align="left"><font face="DejaVu Sans Mono">Perforation, obstruction, toxin, infection, <br>hepatobiliary, pancreatic, <br>female (preggo, ovarian cyst, STI)</font></td>
	</tr>
	<tr>
		<td height="32" align="left"><font face="DejaVu Sans Mono">Chest Pain Diff Dx</font></td>
		<td align="left"><font face="DejaVu Sans Mono">MI, PE, Aortic dissection, GI (GERD, ulcer), <br>Anxiety, Musculoskeletal</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="DejaVu Sans Mono">Acute cough Diff Dx</font></td>
		<td align="left"><font face="DejaVu Sans Mono">Viral, Bacterial, Allergy, </font></td>
	</tr>
	<tr>
		<td height="47" align="left"><font face="DejaVu Sans Mono">Chronic cough Diff Dx</font></td>
		<td align="left"><font face="DejaVu Sans Mono">COPD, Asthma, Allergy, Bacterial, <br>ACE inhibitor, Fungal (Coccidioides), <br>Cystic fibrosis</font></td>
	</tr>
</table>
    """

    table, spans, headers = html2data(html_string)
    for r in range(len(table)):
        print(table[r])

    for s in range(len(spans)):
        print(spans[s])

    string = str(table) + '\n'

    string += str(spans) + '\n'

    f = open('/home/doakey/Desktop/test.txt', 'w')
    f.write(string)
    f.close()
