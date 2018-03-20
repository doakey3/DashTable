from ..dashutils import get_span_row_count


def get_html_row_count(spans):
    """Get the number of rows"""

    if spans == []:
        return 0
    row_counts = {}
    for span in spans:
        span = sorted(span)
        try:
            row_counts[str(span[0][1])] += get_span_row_count(span)
        except KeyError:
            row_counts[str(span[0][1])] = get_span_row_count(span)

    values = list(row_counts.values())
    return max(values)
