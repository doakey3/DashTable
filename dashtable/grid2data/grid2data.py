import itertools

from ..dashutils.make_empty_table import make_empty_table
from ..dashutils.make_span import make_span

def grid2data(text):
    """
    Convert Grid table to data (the kind used by Dashtable)

    Parameters
    ----------
    text : str
        The text must be a valid rst table
    Returns
    -------
    table : list of lists of str
    spans : list of lists of lists of int
        A span is a list of [row, column] pairs that define a group of
        combined table cells
    use_headers : bool
        Whether or not the table was using headers

    Notes
    -----
    This function requires docutils_.

    .. _docutils: http://docutils.sourceforge.net/

    Example
    -------
    >>> text = '''
    ... +------------+------------+-----------+
    ... | Header 1   | Header 2   | Header 3  |
    ... +============+============+===========+
    ... | body row 1 | column 2   | column 3  |
    ... +------------+------------+-----------+
    ... | body row 2 | Cells may span columns.|
    ... +------------+------------+-----------+
    ... | body row 3 | Cells may  | - Cells   |
    ... +------------+ span rows. | - contain |
    ... | body row 4 |            | - blocks. |
    ... +------------+------------+-----------+
    ... '''
    >>> import dashtable
    >>> table, spans, use_headers = dashtable.grid2data(text)
    >>> from pprint import pprint
    >>> pprint(table)
    [['Header 1', 'Header 2', 'Header 3'],
     ['body row 1', 'column 2', 'column 3'],
     ['body row 2', 'Cells may span columns.', ''],
     ['body row 3', 'Cells may\\nspan rows.', '- Cells\\n- contain\\n- blocks.'],
     ['body row 4', '', '']]
    >>> print(spans)
    [[[2, 1], [2, 2]], [[3, 1], [4, 1]], [[3, 2], [4, 2]]]
    >>> print(use_headers)
    True
    """
    try:
        import docutils.statemachine
        import docutils.parsers.rst.tableparser
    except ImportError:
        print("ERROR: You must install the docutils library to use grid2data")
        return

    text = text.strip()
    lines = text.split('\n')
    for i in range(len(lines)):
        lines[i] = lines[i].strip()

    parser = docutils.parsers.rst.tableparser.GridTableParser()
    grid_data = parser.parse(docutils.statemachine.StringList(list(lines)))
    grid_data = list(grid_data)

    column_widths = grid_data.pop(0)
    column_count = len(column_widths)

    if len(grid_data[0]) > 0:
        use_headers = True
        headers = grid_data[0][0]
        row_count = len(grid_data[1]) + 1
        grid_data[1].insert(0, headers)
        grid_data.pop(0)
    else:
        use_headers = False
        grid_data.pop(0)
        row_count = len(grid_data[0])

    grid_data = grid_data[0]
    table = make_empty_table(row_count, column_count)
    spans = []

    for row in range(len(grid_data)):
        for column in range(len(grid_data[row])):
            try:
                text = '\n'.join(grid_data[row][column][3]).rstrip()
                table[row][column] = text
                extra_rows = grid_data[row][column][0]
                extra_columns = grid_data[row][column][1]
                span = make_span(row, column, extra_rows, extra_columns)
                span = sorted(span)
                span = list(span for span,_ in itertools.groupby(span))
                if not len(span) == 1:
                    spans.append(span)
            except TypeError:
                pass

    spans = sorted(spans)
    return table, spans, use_headers
