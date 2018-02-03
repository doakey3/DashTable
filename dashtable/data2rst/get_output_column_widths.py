from ..dashutils import get_span
from ..dashutils import get_span_column_count
from ..dashutils import get_longest_line_length

def get_output_column_widths(table, spans):
    """
    Gets the widths of the columns of the output table

    Parameters
    ----------
    table : list of lists of str
        The table of rows of text
    spans : list of lists of int
        The [row, column] pairs of combined cells

    Returns
    -------
    widths : list of int
        The widths of each column in the output table
    """
    widths = []
    for column in table[0]:
        widths.append(3)

    for row in range(len(table)):
        for column in range(len(table[row])):
            span = get_span(spans, row, column)
            column_count = get_span_column_count(span)

            if column_count == 1:
                text_row = span[0][0]
                text_column = span[0][1]

                text = table[text_row][text_column]

                length = get_longest_line_length(text)
                if length > widths[column]:
                    widths[column] = length

    for row in range(len(table)):
        for column in range(len(table[row])):
            span = get_span(spans, row, column)
            column_count = get_span_column_count(span)

            if column_count > 1:
                text_row = span[0][0]
                text_column = span[0][1]

                text = table[text_row][text_column]

                end_column = text_column + column_count

                available_space = sum(
                    widths[text_column:end_column])
                available_space += column_count - 1

                length = get_longest_line_length(text)

                while length > available_space:
                    for i in range(text_column, end_column):
                        widths[i] += 1

                        available_space = sum(
                            widths[text_column:end_column])

                        available_space += column_count - 1
                        if length <= available_space:
                            break
    return widths
