from ..dashutils import get_span


def extract_spans(html_string):
    """
    Creates a list of the spanned cell groups of [row, column] pairs.

    Parameters
    ----------
    html_string : str

    Returns
    -------
    list of lists of lists of int
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("ERROR: You must have BeautifulSoup to use html2data")
        return

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
                    if not get_span(spans, r_index, c_index):
                        new_span.append([r_index, c_index])

            if len(new_span) > 0:
                spans.append(new_span)

    return spans
