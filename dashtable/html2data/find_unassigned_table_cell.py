def find_unassigned_table_cell(table):
    """
    Search through a table and return the first [row, column] pair
    who's value is None.

    Parameters
    ----------
    table : list of lists of str

    Returns
    -------
    list of int
        The row column pair of the None type cell
    """
    for row in range(len(table)):
        for column in range(len(table[row])):
            if table[row][column] is None:
                return row, column
    return row, column
