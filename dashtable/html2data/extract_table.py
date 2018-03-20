from .find_unassigned_table_cell import find_unassigned_table_cell
from .restructify import restructify

def extract_table(html_string, row_count, column_count):
    """
    Convert an html string to data table

    Parameters
    ----------
    html_string : str
    row_count : int
    column_count : int

    Returns
    -------
    data_table : list of lists of str
    """
    try:
        from bs4 import BeautifulSoup
        from bs4.element import Tag
    except ImportError:
        print("ERROR: You must have BeautifulSoup to use html2data")
        return

    #html_string = convertRichText(html_string)

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
            row, column = find_unassigned_table_cell(data_table)

            r_span_count = 1
            c_span_count = 1

            if td.has_attr('rowspan'):
                r_span_count = int(td['rowspan'])
            if td.has_attr('colspan'):
                c_span_count = int(td['colspan'])

            for row_prime in range(row, row + r_span_count):
                for column_prime in range(column, column + c_span_count):
                    if row_prime == row and column_prime == column:

                        items = []
                        for item in td.contents:
                            items.append(str(item))
                        string = ''.join(items).strip()

                        text = restructify(string).rstrip()

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
