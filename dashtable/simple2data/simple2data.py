import itertools

from .truncate_empty_lines import truncate_empty_lines

from ..dashutils import make_empty_table
from ..dashutils import make_span


def simple2data(text):
    """
    Convert a simple table to data (the kind used by DashTable)

    Parameters
    ----------
    text : str
        A valid simple rst table

    Returns
    -------
    table : list of lists of str
    spans : list of lists of lists of int
        A span is a [row, column] pair that defines a group of merged
        cells in the table. In a simple rst table, spans can only be
        colspans.
    use_headers : bool
        Whether or not this table uses headers
    headers_row : int
        The row where headers are located

    Notes
    -----
    This function requires docutils_.

    .. _docutils: http://docutils.sourceforge.net/

    Example
    -------
    >>> html_text = '''
    ... ======  =====  ======
    ...    Inputs      Output
    ... -------------  ------
    ...   A       B    A or B
    ... ======  =====  ======
    ... False   False  False
    ...  True   False   True
    ... False   True    True
    ...  True   True    True
    ... ======  =====  ======
    ... '''
    >>> from dashtable import simple2data
    >>> table, spans, use_headers, headers_row = simple2data(html_text)
    >>> from pprint import pprint
    >>> pprint(table)
    [['Inputs', 'Output', ''],
     ['A', 'B', 'A or B'],
     ['False', 'False', 'False'],
     ['True, 'False', 'True'],
     ['False', 'True', 'True'],
     ['True', 'True', 'True']]
    >>> print(spans)
    [[[0, 0], [0, 1]]]
    >>> print(use_headers)
    True
    >>> print(headers_row)
    1
    """
    try:
        import docutils.statemachine
        import docutils.parsers.rst.tableparser
    except ImportError:
        print("ERROR: You must install the docutils library to use simple2data")
        return

    lines = text.split('\n')
    lines = truncate_empty_lines(lines)
    leading_space = lines[0].replace(lines[0].lstrip(), '')
    for i in range(len(lines)):
        lines[i] = lines[i][len(leading_space)::]
    parser = docutils.parsers.rst.tableparser.SimpleTableParser()

    block = docutils.statemachine.StringList(list(lines))
    simple_data = list(parser.parse(block))

    column_widths = simple_data.pop(0)
    column_count = len(column_widths)
    headers_row = 0

    if len(simple_data[0]) > 0:
        use_headers = True
        headers_row = len(simple_data[0]) - 1
        headers = simple_data[0][0]
        row_count = len(simple_data[1]) + len(simple_data[0])
        while len(simple_data[0]) > 0:
            simple_data[1].insert(0, simple_data[0][-1])
            simple_data[0].pop(-1)
        simple_data.pop(0)
    else:
        use_headers = False
        simple_data.pop(0)
        row_count = len(simple_data[0])

    simple_data = simple_data[0]
    table = make_empty_table(row_count, column_count)
    spans = []

    for row in range(len(simple_data)):
        for column in range(len(simple_data[row])):
            try:
                text = '\n'.join(simple_data[row][column][3]).rstrip()
                table[row][column] = text
                extra_rows = simple_data[row][column][0]
                extra_columns = simple_data[row][column][1]
                span = make_span(row, column, extra_rows, extra_columns)
                span = sorted(span)
                span = list(span for span,_ in itertools.groupby(span))
                if not len(span) == 1:
                    spans.append(span)
            except TypeError:
                pass
    spans = sorted(spans)
    return table, spans, use_headers, headers_row
