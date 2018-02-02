def row_includes_spans(table, row, spans):
    """
    Determine if there are spans within a row

    Parameters
    ----------
    table : list of lists of str
    row : int
    spans : list of lists of lists of int

    Returns
    -------
    bool
        Whether or not a table's row includes spans
    """
    for column in range(len(table[row])):
        for span in spans:
            if [row, column] in span:
                return True
    return False
