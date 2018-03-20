def get_span_row_count(span):
    """
    Gets the number of rows included in a span

    Parameters
    ----------
    span : list of lists of int
        The [row, column] pairs that make up the span

    Returns
    -------
    rows : int
        The number of rows included in the span

    Example
    -------
    Consider this table::

        +--------+-----+
        | foo    | bar |
        +--------+     |
        | spam   |     |
        +--------+     |
        | goblet |     |
        +--------+-----+

    ::

        >>> span = [[0, 1], [1, 1], [2, 1]]
        >>> print(get_span_row_count(span))
        3
    """
    rows = 1
    first_row = span[0][0]

    for i in range(len(span)):
        if span[i][0] > first_row:
            rows += 1
            first_row = span[i][0]

    return rows
