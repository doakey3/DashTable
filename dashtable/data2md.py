try:
    from .dashutils import lineBreak, centerWord, removeNewlines, addCushions

except SystemError:
    from dashutils import lineBreak, centerWord, removeNewlines, addCushions


def getColumnWidth(column, table):
    width = 3
    for r in range(len(table)):
        w = len(table[r][column])
        if w > width:
            width = w
    return width


def data2md(table):
    """
    Creates a table in the github table format
    """
    table = removeNewlines(table)
    table = addCushions(table)

    widths = []
    for c in range(len(table[0])):
        widths.append(getColumnWidth(c, table))

    output = '|'
    for i in range(len(table[0])):
        output = output + centerWord(widths[i], table[0][i]) + '|'
    output = output + '\n|'
    for i in range(len(table[0])):
        output = output + centerWord(widths[i], lineBreak(widths[i], '-')) + '|'
    output = output + '\n|'

    for r in range(1, len(table)):
        for c in range(len(table[r])):
            output = output + centerWord(widths[c], table[r][c]) + '|'
        output = output + '\n|'

    split = output.split('\n')
    split.pop()

    return '\n'.join(split)


if __name__ == '__main__':

    table = [['column 1', 'col 2', 'c3'],
             ['hspan', 'animal', 'test'],
             ['vspan', 'multispan', 'example']]

    print(data2md(table))
