def get_span_column_count(span):
    """
    Find the length of a colspan.

    Parameters
    ----------
    span : list of lists of int
        The [row, column] pairs that make up the span

    Returns
    -------
    columns : int
        The number of columns included in the span

    Example
    -------
    Consider this table::

        +------+------------------+
        | foo  | bar              |
        +------+--------+---------+
        | spam | goblet | berries |
        +------+--------+---------+

    ::

        >>> span = [[0, 1], [0, 2]]
        >>> print(get_span_column_count(span))
        2
    """
    columns = 1
    first_column = span[0][1]

    for i in range(len(span)):
        if span[i][1] > first_column:
            columns += 1
            first_column = span[i][1]

    return columns
