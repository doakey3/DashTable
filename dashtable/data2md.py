

def lineBreak(count, symbol):
    """makes a string that is count long of symbol"""
    x = ""
    for i in range(0, count):
        x = x + symbol
    return x


def centerWord(spaces, word):
    '''
    given a number of spaces, creates a string that has the word
    centered with half the space on each side.
    '''
    word = word.lstrip().rstrip()
    if len(word) > spaces:
        return word
    extra_space = spaces - len(word)
    space1 = int(extra_space/2)
    space2 = extra_space - space1
    intro = ''
    for i in range(space1):
        intro = intro + ' '
    outro = ''
    for i in range(space2):
        outro = outro + ' '
    string = intro + word + outro
    return string


def cleanTable(table):
    """
    Replaces newlines with ' '
    """
    for r in range(len(table)):
        for c in range(len(table[r])):
            table[r][c] = table[r][c].replace('\n',' ')
    return table


def getColumnWidth(column,table):
    width = -1
    for r in range(len(table)):
        w = len(table[r][column])
        if w > width:
            width = w
    return width + 2


def data2md(table):
    """
    Creates a table in the github table format
    """
    table = cleanTable(table)

    widths = []
    for c in range(len(table[0])):
        widths.append(getColumnWidth(c,table))

    output = '|'
    for i in range(len(table[0])):
        output = output + centerWord(widths[i], table[0][i]) + '|'
    output = output + '\n|'
    for i in range(len(table[0])):
        output = output + centerWord(widths[i], lineBreak(widths[i],'-')) + '|'
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
