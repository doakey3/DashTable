from .cell import get_merge_direction
from .cell import merge_cells


def merge_all_cells(cells):
    """
    Loop through list of cells and piece them together one by one

    Parameters
    ----------
    cells : list of dashtable.data2rst.Cell

    Returns
    -------
    grid_table : str
        The final grid table
    """
    current = 0

    while len(cells) > 1:
        count = 0

        while count < len(cells):
            cell1 = cells[current]
            cell2 = cells[count]

            merge_direction = get_merge_direction(cell1, cell2)
            if not merge_direction == "NONE":
                merge_cells(cell1, cell2, merge_direction)

                if current > count:
                    current -= 1

                cells.pop(count)

            else:
                count += 1

        current += 1

        if current >= len(cells):
            current = 0

    return cells[0].text
