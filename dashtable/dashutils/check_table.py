def check_table(table):
    """
    Ensure the table is valid for converting to grid table.

    * The table must a list of lists
    * Each row must contain the same number of columns
    * The table must not be empty

    Parameters
    ----------
    table : list of lists of str
        The list of rows of strings to convert to a grid table

    Returns
    -------
    message : str
        If no problems are found, this message is empty, otherwise it
        tries to describe the problem that was found.
    """
    if not type(table) is list:
        return "Table must be a list of lists"

    if len(table) == 0:
        return "Table must contain at least one row and one column"

    for i in range(len(table)):
        if not type(table[i]) is list:
            return "Table must be a list of lists"
        if not len(table[i]) == len(table[0]):
            "Each row must have the same number of columns"

    return ""
