import math


def v_center_cell_text(cell):
    """
    Vertically center the text within the cell's grid.

    Like this::

        +--------+     +--------+
        | foobar |     |        |
        |        |     |        |
        |        | --> | foobar |
        |        |     |        |
        |        |     |        |
        +--------+     +--------+

    Parameters
    ----------
    cell : dashtable.data2rst.Cell

    Returns
    -------
    cell : dashtable.data2rst.Cell
    """
    lines = cell.text.split('\n')
    cell_width = len(lines[0]) - 2

    truncated_lines = []
    for i in range(1, len(lines) - 1):
        truncated = lines[i][1:len(lines[i]) - 1]
        truncated_lines.append(truncated)

    total_height = len(truncated_lines)

    empty_lines_above = 0
    for i in range(len(truncated_lines)):
        if truncated_lines[i].rstrip() == '':
            empty_lines_above += 1
        else:
            break

    empty_lines_below = 0
    for i in reversed(range(len(truncated_lines))):
        if truncated_lines[i].rstrip() == '':
            empty_lines_below += 1
        else:
            break

    significant_lines = truncated_lines[
        empty_lines_above:len(truncated_lines) - empty_lines_below
    ]

    remainder = total_height - len(significant_lines)

    blank = cell_width * ' '

    above_height = math.floor(remainder / 2)
    for i in range(0, above_height):
        significant_lines.insert(0, blank)

    below_height = math.ceil(remainder / 2)
    for i in range(0, below_height):
        significant_lines.append(blank)

    for i in range(len(significant_lines)):
        lines[i + 1] = ''.join([
            lines[i + 1][0] + significant_lines[i] + lines[i + 1][-1]
        ])

    cell.text = '\n'.join(lines)

    return cell
