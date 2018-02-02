from ..dashutils import get_span
from ..dashutils import get_span_row_count


def get_output_row_heights(table, spans):
    """
    Get the heights of the rows of the output table.

    Parameters
    ----------
    table : list of lists of str
    spans : list of lists of int

    Returns
    -------
    heights : list of int
        The heights of each row in the output table
    """
    heights = []
    for row in table:
        heights.append(-1)

    for row in range(len(table)):
        for column in range(len(table[row])):
            text = table[row][column]
            span = get_span(spans, row, column)
            row_count = get_span_row_count(span)
            height = len(text.split('\n'))
            if row_count == 1 and height > heights[row]:
                heights[row] = height

    for row in range(len(table)):
        for column in range(len(table[row])):
            span = get_span(spans, row, column)
            row_count = get_span_row_count(span)
            if row_count > 1:
                text_row = span[0][0]
                text_column = span[0][1]

                end_row = text_row + row_count

                text = table[text_row][text_column]

                height = len(text.split('\n')) - (row_count - 1)

                add_row = 0
                while height > sum(heights[text_row:end_row]):
                    heights[text_row + add_row] += 1
                    if add_row + 1 < row_count:
                        add_row += 1
                    else:
                        add_row = 0
    return heights
