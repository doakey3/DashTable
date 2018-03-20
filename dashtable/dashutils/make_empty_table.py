def make_empty_table(row_count, column_count):
    """
    Make an empty table

    Parameters
    ----------
    row_count : int
        The number of rows in the new table
    column_count : int
        The number of columns in the new table

    Returns
    -------
    table : list of lists of str
        Each cell will be an empty str ('')
    """
    table = []
    while row_count > 0:
        row = []
        for column in range(column_count):
            row.append('')
        table.append(row)
        row_count -= 1
    return table
