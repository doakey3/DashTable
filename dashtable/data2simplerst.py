import math

def space_fill(count, symbol):
    """makes a string that is count long of symbol"""
    x = ""
    for i in range(0, count):
        x = x + symbol
    return x

def center_word(space, line):
    """Centers text to available space"""
    left = math.floor((space - len(line)) / 2)
    right = math.ceil((space - len(line)) / 2)
    
    left_space = space_fill(left, ' ')
    right_space = space_fill(right, ' ')
        
    line = left_space + line + right_space
    return line

def getSpanColumnCount(span):
    """Gets the number of columns inluded in a span"""
    columns = 1
    first_column = span[0][1]
    for i in range(len(span)):
        if span[i][1] > first_column:
            columns += 1
            first_column = span[i][1]
    return columns

def includes_spans(table, row, spans):
    for column in range(len(table[row])):
        for span in spans:
            if [row, column] in span:
                return True
    return False
    
def in_spans(row, column, spans):
    for span in spans:
        if [row, column] in span:
            return True
    return False

def get_span(row, column, spans):
    for span in spans:
        if [row, column] in span:
            return span
    return None

def data2simplerst(table, spans, use_headers=True, headers_row=0):
    '''Convert table data to a simple rst table'''
    
    output = []
    
    column_widths = []
    for col in table[0]:
        column_widths.append(0)
    for row in range(len(table)):
        for column in range(len(table[row])):
            if len(table[row][column]) > column_widths[column]:
                column_widths[column] = len(table[row][column])
    underline = ''
    for col in column_widths:
        underline = underline + space_fill(col, '=') + '  '
        
    output.append(underline)
    
    for row in range(len(table)):
        string = ''
        column = 0
        while column < len(table[row]):
            span = get_span(row, column, spans)
            if span and span[0] == [row, column] and not table[row][column] == '':
                span_col_count = getSpanColumnCount(span)
                width = sum(column_widths[column:column + span_col_count]) + (2 * (span_col_count - 1))
                string += center_word(width, table[row][column]) + '  '
            elif table[row][column] == '':
                pass
            else:
                string += center_word(column_widths[column], table[row][column]) + '  '
            column += 1
                
        output.append(string)
        if row == headers_row and use_headers == True:
            output.append(underline)
        else:
            if includes_spans(table, row, spans):
                new_underline = ''
                column = 0
                while column < len(table[row]):
                    span = get_span(row, column, spans)
                    if span and span[0] == [row, column] and not table[row][column] == '':
                        span_col_count = getSpanColumnCount(span)
                        width = sum(column_widths[column:column + span_col_count]) + (2 * (span_col_count - 1))
                        new_underline += space_fill(width, '-') + '  '
                    elif table[row][column] == '':
                        pass
                    else:
                        new_underline += space_fill(column_widths[column], '-') + '  '
                    column += 1
                output.append(new_underline)
    for i in range(len(output)):
        output[i] = output[i].rstrip()
    output.append(underline)
    return '\n'.join(output)
