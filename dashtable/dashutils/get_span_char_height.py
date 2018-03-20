from .get_span_row_count import get_span_row_count


def get_span_char_height(span, row_heights):
    """
    Get the height of a span in the number of newlines it fills.

    Parameters
    ----------
    span : list of list of int
        A list of [row, column] pairs that make up the span
    row_heights : list of int
        A list of the number of newlines for each row in the table

    Returns
    -------
    total_height : int
        The height of the span in number of newlines
    """
    start_row = span[0][0]
    row_count = get_span_row_count(span)
    total_height = 0

    for i in range(start_row, start_row + row_count):
        total_height += row_heights[i]
    total_height += row_count - 1

    return total_height
