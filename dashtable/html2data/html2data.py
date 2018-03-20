from .extract_spans import extract_spans
from .get_html_column_count import get_html_column_count
from .get_html_row_count import get_html_row_count
from .extract_table import extract_table
from .headers_present import headers_present

def html2data(html_string):
    """
    Convert an html table to a data table and spans.

    Parameters
    ----------
    html_string : str
        The string containing the html table

    Returns
    -------
    table : list of lists of str
    spans : list of lists of lists of int
        A span is a list of [row, column] pairs that define what cells
        are merged in a table.
    use_headers : bool
    """
    spans = extract_spans(html_string)

    column_count = get_html_column_count(html_string)
    row_count = get_html_row_count(spans)

    count = 0
    while count < len(spans):
        if len(spans[count]) == 1:
            spans.pop(count)
        else:
            count += 1

    table = extract_table(html_string, row_count, column_count)

    use_headers = headers_present(html_string)

    return table, spans, use_headers
