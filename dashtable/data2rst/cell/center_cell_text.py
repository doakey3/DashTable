import math
from .get_longest_line_length import get_longest_line_length

def center_cell_text(cell):
    """
    Horizontally center the text within a cell's grid

    Like this::

        +---------+     +---------+
        | foo     | --> |   foo   |
        +---------+     +---------+

    Parameters
    ----------
    cell : dashtable.data2rst.Cell

    Returns
    -------
    cell : dashtable.data2rst.Cell
    """
    lines = cell.text.split('\n')
    cell_width = len(lines[0]) - 2

    truncated_lines = ['']
    for i in range(1, len(lines) - 1):
        truncated = lines[i][2:len(lines[i]) - 2].rstrip()
        truncated_lines.append(truncated)

    truncated_lines.append('')

    max_line_length = get_longest_line_length('\n'.join(truncated_lines))
    remainder = cell_width - max_line_length

    left_width = math.floor(remainder / 2)
    left_space = left_width * ' '

    for i in range(len(truncated_lines)):
        truncated_lines[i] = left_space + truncated_lines[i]
        right_width = cell_width - len(truncated_lines[i])
        truncated_lines[i] += right_width * ' '

    for i in range(1, len(lines) - 1):
        lines[i] = ''.join([
            lines[i][0], truncated_lines[i], lines[i][-1]
        ])

    cell.text = '\n'.join(lines)

    return cell
