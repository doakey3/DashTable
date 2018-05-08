from .get_output_column_widths import get_output_column_widths
from .get_output_row_heights import get_output_row_heights

from ..dashutils import add_cushions
from ..dashutils import ensure_table_strings
from ..dashutils.check_table import check_table
from ..dashutils.check_span import check_span

from .make_cell import make_cell
from .table_cells_2_spans import table_cells_2_spans
from .merge_all_cells import merge_all_cells

from .cell import center_cell_text
from .cell import v_center_cell_text

import copy


def data2rst(table, spans=[[[0, 0]]], use_headers=True,
             center_cells=False, center_headers=False):
    """
    Convert a list of lists of str into a reStructuredText Grid Table

    Parameters
    ----------
    table : list of lists of str
    spans : list of lists of lists of int, optional
        These are [row, column] pairs of cells that are merged in the
        table. Rows and columns start in the top left of the table.For
        example::

            +--------+--------+
            | [0, 0] | [0, 1] |
            +--------+--------+
            | [1, 0] | [1, 1] |
            +--------+--------+

    use_headers : bool, optional
        Whether or not the first row of table data will become headers.
    center_cells : bool, optional
        Whether or not cells will be centered
    center_headers: bool, optional
        Whether or not headers will be centered

    Returns
    -------
    str
        The grid table string

    Example
    -------
    >>> spans = [
    ...     [ [3, 1], [4, 1] ],
    ...     [ [3, 2], [4, 2] ],
    ...     [ [2, 1], [2, 2] ],
    ... ]
    >>> table = [
    ...     ["Header 1", "Header 2", "Header 3"],
    ...     ["body row 1", "column 2", "column 3"],
    ...     ["body row 2", "Cells may span columns", ""],
    ...     ["body row 3", "Cells may span rows.", "- Cells\\n-contain\\n-blocks"],
    ...     ["body row 4", "", ""],
    ... ]
    >>> print(dashtable.data2rst(table, spans))
    +------------+------------+-----------+
    | Header 1   | Header 2   | Header 3  |
    +============+============+===========+
    | body row 1 | column 2   | column 3  |
    +------------+------------+-----------+
    | body row 2 | Cells may span columns.|
    +------------+------------+-----------+
    | body row 3 | Cells may  | - Cells   |
    +------------+ span rows. | - contain |
    | body row 4 |            | - blocks. |
    +------------+------------+-----------+
    """

    table = copy.deepcopy(table)

    table_ok = check_table(table)
    if not table_ok == "":
        return "ERROR: " + table_ok

    if not spans == [[[0, 0]]]:
        for span in spans:
            span_ok = check_span(span, table)
            if not span_ok == "":
                return "ERROR: " + span_ok

    table = ensure_table_strings(table)
    table = add_cushions(table)

    spans = table_cells_2_spans(table, spans)

    widths = get_output_column_widths(table, spans)
    heights = get_output_row_heights(table, spans)

    cells = []
    for span in spans:
        cell = make_cell(table, span, widths, heights, use_headers)
        cells.append(cell)

    cells = list(sorted(cells))

    if center_cells:
        for cell in cells:
            if not cell.is_header:
                center_cell_text(cell)
                v_center_cell_text(cell)

    if center_headers:
        for cell in cells:
            if cell.is_header:
                center_cell_text(cell)
                v_center_cell_text(cell)

    grid_table = merge_all_cells(cells)

    return grid_table

