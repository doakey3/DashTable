def get_span(spans, row, column):
    """
    Gets the span containing the [row, column] pair

    Parameters
    ----------
    spans : list of lists of lists
        A list containing spans, which are lists of [row, column] pairs
        that define where a span is inside a table.

    Returns
    -------
    span : list of lists
        A span containing the [row, column] pair
    """
    for i in range(len(spans)):
        if [row, column] in spans[i]:
            return spans[i]

    return None

