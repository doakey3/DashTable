from .get_span_column_count import get_span_column_count


def get_span_char_width(span, column_widths):
    """
    Sum the widths of the columns that make up the span, plus the extra.

    Parameters
    ----------
    span : list of lists of int
        list of [row, column] pairs that make up the span
    column_widths : list of int
        The widths of the columns that make up the table

    Returns
    -------
    total_width : int
        The total width of the span
    """

    start_column = span[0][1]
    column_count = get_span_column_count(span)
    total_width = 0

    for i in range(start_column, start_column + column_count):
        total_width += column_widths[i]

    total_width += column_count - 1

    return total_width
