def get_merge_direction(cell1, cell2):
    """
    Determine the side of cell1 that can be merged with cell2.

    This is based on the location of the two cells in the table as well
    as the compatability of their height and width.

    For example these cells can merge::

         cell1    cell2      merge "RIGHT"

        +-----+  +------+   +-----+------+
        | foo |  | dog  |   | foo | dog  |
        |     |  +------+   |     +------+
        |     |  | cat  |   |     | cat  |
        |     |  +------+   |     +------+
        |     |  | bird |   |     | bird |
        +-----+  +------+   +-----+------+

    But these cells cannot merge::

        +-----+  +------+
        | foo |  | dog  |
        |     |  +------+
        |     |  | cat  |
        |     |  +------+
        |     |
        +-----+

    Parameters
    ----------
    cell1 : dashtable.data2rst.Cell
    cell2 : dashtable.data2rst.Cell

    Returns
    -------
    str
        The side onto which cell2 can be merged. Will be one of
        ["LEFT", "RIGHT", "BOTTOM", "TOP", "NONE"]
    """
    cell1_left = cell1.column
    cell1_right = cell1.column + cell1.column_count
    cell1_top = cell1.row
    cell1_bottom = cell1.row + cell1.row_count

    cell2_left = cell2.column
    cell2_right = cell2.column + cell2.column_count
    cell2_top = cell2.row
    cell2_bottom = cell2.row + cell2.row_count

    if (cell1_right == cell2_left and cell1_top == cell2_top and
            cell1_bottom == cell2_bottom and
            cell1.right_sections >= cell2.left_sections):
        return "RIGHT"

    elif (cell1_left == cell2_left and cell1_right == cell2_right and
            cell1_top == cell2_bottom and
            cell1.top_sections >= cell2.bottom_sections):
        return "TOP"

    elif (cell1_left == cell2_left and
          cell1_right == cell2_right and
          cell1_bottom == cell2_top and
          cell1.bottom_sections >= cell2.top_sections):
        return "BOTTOM"

    elif (cell1_left == cell2_right and
          cell1_top == cell2_top and
          cell1_bottom == cell2_bottom and
          cell1.left_sections >= cell2.right_sections):
        return "LEFT"

    else:
        return "NONE"
