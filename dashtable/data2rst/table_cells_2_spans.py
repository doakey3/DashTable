from ..dashutils import get_span


def table_cells_2_spans(table, spans):
    """
    Converts the table to a list of spans, for consistency.

    This method combines the table data with the span data into a
    single, more consistent type. Any normal cell will become a span
    of just 1 column and 1 row.

    Parameters
    ----------
    table : list of lists of str
    spans : list of lists of int

    Returns
    -------
    table : list of lists of lists of int
        As you can imagine, this is pretty confusing for a human which
        is why data2rst accepts table data and span data separately.
    """
    new_spans = []
    for row in range(len(table)):
        for column in range(len(table[row])):
            span = get_span(spans, row, column)

            if not span:
                new_spans.append([[row, column]])

    new_spans.extend(spans)
    new_spans = list(sorted(new_spans))

    return new_spans

