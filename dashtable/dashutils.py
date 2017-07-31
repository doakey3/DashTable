import math

def getSpanColumnCount(span):
    """Gets the number of columns inluded in a span"""
    columns = 1
    first_column = span[0][1]
    for i in range(len(span)):
        if span[i][1] > first_column:
            columns += 1
            first_column = span[i][1]
    return columns


def getSpanRowCount(span):
    """Gets the number of rows included in a span"""
    rows = 1
    first_row = span[0][0]
    for i in range(len(span)):
        if span[i][0] > first_row:
            rows += 1
            first_row = span[i][0]
    return rows


def sortSpans(spans):
    """Ensure the first cell of each span is the text cell"""
    for span in range(len(spans)):
        spans[span] = sorted(spans[span])
    return spans


def getSpan(spans, row, column):
    """checks if a row,column is in spans"""
    for i in range(len(spans)):
        if [row, column] in spans[i]:
            return spans[i]
    return None


def lineBreak(count, symbol):
    """makes a string that is count long of symbol"""
    x = ""
    for i in range(0, count):
        x = x + symbol
    return x


def centerWord(space, line):
    """Centers text to available space"""
    left = math.floor((space - len(line)) / 2)
    right = math.ceil((space - len(line)) / 2)
    
    left_space = lineBreak(left, ' ')
    right_space = lineBreak(right, ' ')
        
    line = left_space + line + right_space
    return line


def addCushions(table):
    """adds space to start and end of each item in a list of lists"""
    for row in range(len(table)):
        for column in range(len(table[row])):
            lines = table[row][column].split("\n")
            for i in range(len(lines)):
                if not lines[i] == "":
                    lines[i] = " " + lines[i].rstrip() + " "
            table[row][column] = "\n".join(lines)
    return table


def removeNewlines(table):
    """
    Replaces newlines with ' '
    """
    for r in range(len(table)):
        for c in range(len(table[r])):
            table[r][c] = table[r][c].replace('\n', ' ')
    return table
