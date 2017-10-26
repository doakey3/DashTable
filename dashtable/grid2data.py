import docutils.statemachine
import docutils.parsers.rst.tableparser
import itertools

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

def grid2data(text):
    '''Convert Grid table to data (the kind used by Dashtable'''
    
    text = text.strip()
    
    parser = docutils.parsers.rst.tableparser.GridTableParser()
    lines = text.split('\n')
    grid_data = parser.parse(docutils.statemachine.StringList(list(lines)))
    grid_data = list(grid_data)
    
    column_widths = grid_data.pop(0)
    column_count = len(column_widths)
    
    if len(grid_data[0]) > 0:
        use_headers = True
        headers = grid_data[0][0]
        row_count = len(grid_data[1]) + 1
        grid_data[1].insert(0, headers)
        grid_data.pop(0)
    else:
        use_headers = False
        grid_data.pop(0)
        
    grid_data = grid_data[0]
    table = make_empty_table(row_count, column_count)
    spans = []
    
    for row in range(len(grid_data)):
        for column in range(len(grid_data[row])):
            try:
                text = '\n'.join(grid_data[row][column][3]).rstrip()
                table[row][column] = text
                extra_rows = grid_data[row][column][0]
                extra_columns = grid_data[row][column][1]
                span = make_span(row, column, extra_rows, extra_columns)
                span = sorted(span)
                span = list(span for span,_ in itertools.groupby(span))
                if not len(span) == 1:
                    spans.append(span)
            except TypeError:
                pass
    spans = sorted(spans)
    return table, spans, use_headers
