from ..dashutils import get_span_char_width
from ..dashutils import get_span_char_height
from ..dashutils import get_span_row_count
from ..dashutils import get_span_column_count

from .cell import Cell


def make_cell(table, span, widths, heights, use_headers):
    """
    Convert the contents of a span of the table to a grid table cell

    Parameters
    ----------
    table : list of lists of str
        The table of rows containg strings to convert to a grid table
    span : list of lists of int
        list of [row, column] pairs that make up a span in the table
    widths : list of int
        list of the column widths of the table
    heights : list of int
        list of the heights of each row in the table
    use_headers : bool
        Whether or not to use headers in the table

    Returns
    -------
    cell : dashtable.data2rst.Cell
    """
    width = get_span_char_width(span, widths)
    height = get_span_char_height(span, heights)
    text_row = span[0][0]
    text_column = span[0][1]
    text = table[text_row][text_column]

    lines = text.split("\n")
    for i in range(len(lines)):
        width_difference = width - len(lines[i])
        lines[i] = ''.join([lines[i], " " * width_difference])

    height_difference = height - len(lines)
    empty_lines = []
    for i in range(0, height_difference):
        empty_lines.append(" " * width)
    lines.extend(empty_lines)

    output = [
        ''.join(["+", (width * "-") + "+"])
    ]

    for i in range(0, height):
        output.append("|" + lines[i] + "|")

    if use_headers and span[0][0] == 0:
        symbol = "="
    else:
        symbol = "-"

    output.append(
        ''.join(["+", width * symbol, "+"])
    )

    text = "\n".join(output)

    row_count = get_span_row_count(span)
    column_count = get_span_column_count(span)

    cell = Cell(text, text_row, text_column, row_count, column_count)

    return cell
