from ..dashutils import ensure_table_strings
from ..dashutils.check_table import check_table
from ..dashutils.check_span import check_span
from ..dashutils.multis_2_mono import multis_2_mono
from ..dashutils.center_line import center_line
from ..dashutils.get_span_column_count import get_span_column_count
from ..dashutils.get_span import get_span

from .row_includes_spans import row_includes_spans

import copy

def data2simplerst(table, spans=[[[0, 0]]], use_headers=True, headers_row=0):
    """
    Convert table data to a simple rst table

    Parameters
    ----------
    table : list of lists of str
        A table of strings.
    spans : list of lists of lists of int
        A list of spans. A span is a list of [Row, Column] pairs of
        table cells that are joined together.
    use_headers : bool, optional
        Whether or not to include headers in the table. A header is
        a cell that is underlined with "="
    headers_row : int
        The row that will be the headers. In a simple rst table, the
        headers do not need to be at the top.

    Returns
    -------
    str
        The simple rst table

    Example
    -------
    >>> table = [
    ...     ["Inputs", "", "Output"],
    ...     ["A", "B", "A or B"],
    ...     ["False", "False", "False"],
    ...     ["True", "False", "True"],
    ...     ["False", "True", "True"],
    ...     ["True", "True", "True"],
    ... ]
    >>> spans = [
    ...     [ [0, 0], [0, 1] ]
    ... ]
    >>> print(data2simplerst(table, spans, headers_row=1))
    ======  =====  ======
       Inputs      Output
    -------------  ------
      A       B    A or B
    ======  =====  ======
    False   False  False
     True   False   True
    False   True    True
     True   True    True
    ======  =====  ======
    """

    table = copy.deepcopy(table)

    table_ok = check_table(table)
    if not table_ok == "":
        return "ERROR: " + table_ok

    if not spans == [[[0, 0]]]:
        for span in spans:
            span_ok = check_span(span, table)
            if not span_ok == "":
                return "ERROR: " + span_ok

    table = ensure_table_strings(table)
    table = multis_2_mono(table)

    output = []

    column_widths = []
    for col in table[0]:
        column_widths.append(0)
    for row in range(len(table)):
        for column in range(len(table[row])):
            if len(table[row][column]) > column_widths[column]:
                column_widths[column] = len(table[row][column])

    underline = ''
    for col in column_widths:
        underline = ''.join([underline + col * '=', '  '])

    output.append(underline)

    for row in range(len(table)):
        string = ''
        column = 0

        while column < len(table[row]):
            span = get_span(spans, row, column)

            if (span and span[0] == [row, column] and
                    not table[row][column] == ''):
                span_col_count = get_span_column_count(span)

                end_col = column + span_col_count
                width = sum(column_widths[column:end_col])
                width += 2 * (span_col_count - 1)

                string += center_line(width, table[row][column]) + '  '

            elif table[row][column] == '':
                pass

            else:
                string += center_line(
                    column_widths[column], table[row][column]) + '  '

            column += 1

        output.append(string)

        if row == headers_row and use_headers:
            output.append(underline)

        else:
            if row_includes_spans(table, row, spans):
                new_underline = ''
                column = 0
                while column < len(table[row]):
                    span = get_span(spans, row, column)
                    if (span and span[0] == [row, column] and
                            not table[row][column] == ''):
                        span_col_count = get_span_column_count(span)

                        end_column = column + span_col_count
                        width = sum(column_widths[column:end_column])
                        width += 2 * (span_col_count - 1)

                        new_underline += (width * '-') + '  '

                    elif table[row][column] == '':
                        pass

                    else:
                        new_underline += (column_widths[column] * '-') + '  '
                    column += 1
                output.append(new_underline)

    for i in range(len(output)):
        output[i] = output[i].rstrip()

    output.append(underline)

    return '\n'.join(output)
