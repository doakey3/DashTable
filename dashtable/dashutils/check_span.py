import copy

from .get_span_row_count import get_span_row_count
from .get_span_column_count import get_span_column_count


def check_span(span, table):
    """
    Ensure the span is valid.

    A span is a list of [row, column] pairs. These coordinates
    must form a rectangular shape. For example, this span will cause an
    error because it is not rectangular in shape.::

        span = [[0, 1], [0, 2], [1, 0]]

    Spans must be

        * Rectanglular
        * A list of lists of int
        *

    Parameters
    ----------
    span : list of lists of int
    table : list of lists of str

    Return
    ------
    exception_string : str
        A message that states there was something wrong.
    """

    if not type(span) is list:
        return "Spans must be a list of lists"

    for pair in span:
        if not type(pair) is list:
            return "Spans must be a list of lists of int"
        if not len(pair) == 2:
            return "Spans must be a [Row, Column] pair of integers"

    total_rows = get_span_row_count(span)
    total_columns = get_span_column_count(span)

    if not len(span) == total_rows * total_columns:
        return ''.join(["Spans must be rectangular in shape. ",
                        str(span) + " is invalid"])

    if max(span, key=lambda x: x[0])[0] > len(table) - 1:
        return ' '.join(["One of the span's rows extends beyond the",
                         "bounds of the table:", str(span)])

    if max(span, key=lambda x: x[1])[1] > len(table[0]) - 1:
        return ' '.join(["One of the span's columns extends beyond the",
                         "bounds of the table:", str(span)])

    test_span = copy.deepcopy(span)

    checked = [test_span.pop(0)]

    while len(test_span) > 0:
        row = test_span[0][0]
        col = test_span[0][1]
        matched = False

        for i in range(len(checked)):
            if row == checked[i][0] and abs(col - checked[i][1]) == 1:
                matched = True

            elif abs(row - checked[i][0]) == 1 and col == checked[i][1]:
                matched = True

        if matched:
            checked.append(test_span.pop(0))

        else:
            checked.extend(test_span)
            return 'This span is not valid: ' + str(checked)

    return ""
