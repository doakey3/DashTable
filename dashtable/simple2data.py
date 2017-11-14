import docutils.statemachine
import docutils.parsers.rst.tableparser
import itertools

def truncate_empties(lines):
    while lines[0].rstrip() == '':
        lines.pop(0)
    while lines[len(lines) - 1].rstrip() == '':
        lines.pop(-1)
    return lines
    
def make_empty_table(row_count, column_count):
    table = []
    while row_count > 0:
        row = []
        for column in range(column_count):
            row.append('')
        table.append(row)
        row_count -= 1
    return table
    
def make_span(row, column, extra_rows, extra_columns):
    span = [[row, column]]
    for r in range(row, row + extra_rows + 1):
        span.append([r, column])
    for c in range(column, column + extra_columns + 1):
        span.append([row, c])
    span.append([r, c])
    
    return span

def simple2data(text):
    '''Convert a simple table to data (the kind used by DashTable'''
    lines = text.split('\n')
    lines = truncate_empties(lines)
    leading_space = lines[0].replace(lines[0].lstrip(), '')
    for i in range(len(lines)):
        lines[i] = lines[i][len(leading_space)::]
    parser = docutils.parsers.rst.tableparser.SimpleTableParser()

    block = docutils.statemachine.StringList(list(lines))
    simple_data = list(parser.parse(block))
    
    column_widths = simple_data.pop(0)
    column_count = len(column_widths)
    headers_row = 0
    
    if len(simple_data[0]) > 0:
        use_headers = True
        headers_row = len(simple_data[0]) - 1
        headers = simple_data[0][0]
        row_count = len(simple_data[1]) + len(simple_data[0])
        while len(simple_data[0]) > 0:
            simple_data[1].insert(0, simple_data[0][-1])
            simple_data[0].pop(-1)
        simple_data.pop(0)
    else:
        use_headers = False
        simple_data.pop(0)
        row_count = len(simple_data[0])
    
    simple_data = simple_data[0]
    table = make_empty_table(row_count, column_count)
    spans = []
    
    for row in range(len(simple_data)):
        for column in range(len(simple_data[row])):
            try:
                text = '\n'.join(simple_data[row][column][3]).rstrip()
                table[row][column] = text
                extra_rows = simple_data[row][column][0]
                extra_columns = simple_data[row][column][1]
                span = make_span(row, column, extra_rows, extra_columns)
                span = sorted(span)
                span = list(span for span,_ in itertools.groupby(span))
                if not len(span) == 1:
                    spans.append(span)
            except TypeError:
                pass
    spans = sorted(spans)
    return table, spans, use_headers, headers_row
