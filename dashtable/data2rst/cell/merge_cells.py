def merge_cells(cell1, cell2, direction):
    """
    Combine the side of cell1's grid text with cell2's text.

    For example::

         cell1    cell2      merge "RIGHT"

        +-----+  +------+   +-----+------+
        | foo |  | dog  |   | foo | dog  |
        |     |  +------+   |     +------+
        |     |  | cat  |   |     | cat  |
        |     |  +------+   |     +------+
        |     |  | bird |   |     | bird |
        +-----+  +------+   +-----+------+

    Parameters
    ----------
    cell1 : dashtable.data2rst.Cell
    cell2 : dashtable.data2rst.Cell
    """

    cell1_lines = cell1.text.split("\n")
    cell2_lines = cell2.text.split("\n")

    if direction == "RIGHT":
        for i in range(len(cell1_lines)):
            cell1_lines[i] = cell1_lines[i] + cell2_lines[i][1::]
        cell1.text = "\n".join(cell1_lines)
        cell1.column_count += cell2.column_count

    elif direction == "TOP":
        if cell1_lines[0].count('+') > cell2_lines[-1].count('+'):
            cell2_lines.pop(-1)
        else:
            cell1_lines.pop(0)
        cell2_lines.extend(cell1_lines)
        cell1.text = "\n".join(cell2_lines)
        cell1.row_count += cell2.row_count
        cell1.row = cell2.row
        cell1.column = cell2.column

    elif direction == "BOTTOM":
        if (cell1_lines[-1].count('+') > cell2_lines[0].count('+') or
                cell1.is_header):
            cell2_lines.pop(0)
        else:
            cell1_lines.pop(-1)
        cell1_lines.extend(cell2_lines)
        cell1.text = "\n".join(cell1_lines)
        cell1.row_count += cell2.row_count

    elif direction == "LEFT":
        for i in range(len(cell1_lines)):
            cell1_lines[i] = cell2_lines[i][0:-1] + cell1_lines[i]
        cell1.text = "\n".join(cell1_lines)
        cell1.column_count += cell2.column_count
        cell1.row = cell2.row
        cell1.column = cell2.column


