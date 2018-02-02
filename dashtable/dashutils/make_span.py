def make_span(row, column, extra_rows, extra_columns):
    """
    Create a list of rows and columns that will make up a span

    Parameters
    ----------
    row : int
        The row of the first cell in the span
    column : int
        The column of the first cell in the span
    extra_rows : int
        The number of rows that make up the span
    extra_columns : int
        The number of columns that make up the span

    Returns
    -------
    span : list of lists of int
        A span is a list of [row, column] pairs that make up a span
    """
    span = [[row, column]]

    for r in range(row, row + extra_rows + 1):
        span.append([r, column])

    for c in range(column, column + extra_columns + 1):
        span.append([row, c])
    span.append([r, c])

    return span
