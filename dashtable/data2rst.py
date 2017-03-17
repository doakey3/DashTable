try:
    from .dashutils import lineBreak, getSpan, getSpanColumnCount
    from .dashutils import sortSpans, addCushions

except SystemError:
    from dashutils import lineBreak, getSpan, getSpanColumnCount
    from dashutils import sortSpans, addCushions


class Cell():
    """Holds the text and data for an rst text cell"""
    def __init__(self, text, row, column, row_count, column_count):
        self.text = text
        self.row = row
        self.column = column
        self.row_count = row_count
        self.column_count = column_count

    def __lt__(self, other):
        """For sorting instances of this class"""
        return [self.row, self.column] < [other.row, other.column]

    def mergeableDirection(self, other):
        """Determines the direction in which two cells can be merged"""
        self_left = self.column
        self_right = self.column + self.column_count
        self_top = self.row
        self_bottom = self.row + self.row_count

        other_left = other.column
        other_right = other.column + other.column_count
        other_top = other.row
        other_bottom = other.row + other.row_count

        if (self_right == other_left and self_top == other_top and
                self_bottom == other_bottom):
            return "RIGHT"
        elif (self_left == other_left and self_right == other_right and
                self_top == other_bottom):
            return "TOP"
        elif (self_left == other_left and
              self_right == other_right and
              self_bottom == other_top):
            return "BOTTOM"
        elif (self_left == other_right and
              self_top == other_top and
              self_bottom == other_bottom):
            return "LEFT"
        else:
            return "NONE"

    def merge(self, other):
        """attempts to merge two cells"""

        self_lines = self.text.split("\n")
        other_lines = other.text.split("\n")

        if self.mergeableDirection(other) == "RIGHT":
            for i in range(len(self_lines)):
                self_lines[i] = self_lines[i] + other_lines[i][1::]
            self.text = "\n".join(self_lines)
            self.column_count += other.column_count
            return True
        elif self.mergeableDirection(other) == "TOP":
            self_lines.pop(0)
            other_lines.extend(self_lines)
            self.text = "\n".join(other_lines)
            self.row_count += other.row_count
            self.row = other.row
            self.column = other.column
            return True
        elif self.mergeableDirection(other) == "BOTTOM":
            other_lines.pop(0)
            self_lines.extend(other_lines)
            self.text = "\n".join(self_lines)
            self.row_count += other.row_count
            return True
        elif self.mergeableDirection(other) == "LEFT":
            for i in range(len(self_lines)):
                self_lines[i] = other_lines[i] + self_lines[i][1::]
            self.text = "\n".join(self_lines)
            self.column_count += other.column_count
            self.row = other.row
            self.column = other.column
            return True
        else:
            return False


def getLongestLineLength(text):
    """Get the length longest line in a paragraph"""
    lines = text.split("\n")
    length = 0
    for i in range(len(lines)):
        if len(lines[i]) > length:
            length = len(lines[i])
    return length


def getSpanRowCount(span):
    """Gets the number of rows included in a span"""
    rows = 1
    first_row = span[0][0]
    for i in range(len(span)):
        if span[i][0] > first_row:
            rows += 1
            first_row = span[i][0]
    return rows


def getTotalSpanHeight(span, heights):
    """Sum the row heights of a span"""
    start_row = span[0][0]
    row_count = getSpanRowCount(span)
    total_height = 0
    for i in range(start_row, start_row + row_count):
        total_height += heights[i]
    total_height += row_count - 1
    return total_height


def getTotalSpanWidth(span, widths):
    """Sum the widths of a span"""
    start_column = span[0][1]
    column_count = getSpanColumnCount(span)
    total_width = 0
    for i in range(start_column, start_column + column_count):
        total_width += widths[i]
    total_width += column_count - 1
    return total_width


def mergeCells(cells):
    """Loop through list of cells and piece them together one by one"""
    current = 0
    while len(cells) > 1:
        count = 0
        while count < len(cells):
            if cells[current].merge(cells[count]):
                if current > count:
                    current -= 1
                cells.pop(count)
            else:
                count += 1
        current += 1
        if current >= len(cells):
            current = 0
    return cells[0].text


def makeTextCell(table, span, widths, heights, use_headers):
    """Creates an rst text Cell"""
    width = getTotalSpanWidth(span, widths)
    height = getTotalSpanHeight(span, heights)
    text_row = span[0][0]
    text_column = span[0][1]
    text = table[text_row][text_column]

    lines = text.split("\n")
    for i in range(len(lines)):
        width_difference = width - len(lines[i])
        lines[i] = lines[i] + lineBreak(width_difference, " ")

    height_difference = height - len(lines)
    empty_lines = []
    for i in range(0, height_difference):
        empty_lines.append(lineBreak(width, " "))
    lines.extend(empty_lines)

    output = ["+" + lineBreak(width, "-") + "+"]
    for i in range(0, height):
        output.append("|" + lines[i] + "|")

    if use_headers and span[0][0] == 0:
        symbol = "="
    else:
        symbol = "-"
    output.append("+" + lineBreak(width, symbol) + "+")

    text = "\n".join(output)
    row_count = getSpanRowCount(span)
    column_count = getSpanColumnCount(span)
    cell = Cell(text, text_row, text_column, row_count, column_count)

    return cell


def getHeights(table, spans):
    """get the heights of the rows of the output table"""
    span_remainders = {}
    for span in spans:
        span_remainders[str(span)] = 0

    heights = []
    for row in table:
        heights.append(-1)

    for row in range(len(table)):
        for column in range(len(table[row])):
            span = getSpan(spans, row, column)
            text_row = span[0][0]
            text_column = span[0][1]
            text = table[text_row][text_column]
            row_count = getSpanRowCount(span)
            avg = len(text.split("\n")) / row_count
            key = str(span)
            if avg > heights[row]:
                span_remainders[key] += avg - int(avg)
                heights[row] = int(avg)
            elif avg + span_remainders[key] < heights[row]:
                span_remainders[key] += avg - int(avg)
            elif avg + span_remainders[key] == heights[row]:
                span_remainders[key] = 0
            elif avg + span_remainders[key] > heights[row]:
                heights[row] = int(avg + span_remainders[key])
                span_remainders[key] += avg
                span_remainders[key] -= int(span_remainders[key])
    return heights

def getSimpleWidths(table, spans):
    """Assign widths to all columns based only on single-column spans"""
    widths = []
    for column in table[0]:
        widths.append(3)

    for row in range(len(table)):
        for column in range(len(table[row])):
            span = getSpan(spans, row, column)
            column_count = getSpanColumnCount(span)
            if column_count == 1:
                text_row = span[0][0]
                text_column = span[0][1]
                text = table[text_row][text_column]
                length = getLongestLineLength(text)
                if length > widths[column]:
                    widths[column] = length
    return widths

def getWidths(table, spans):
    """Get the widths of the columns of the output table"""

    widths = getSimpleWidths(table, spans)

    for row in range(len(table)):
        for column in range(len(table[row])):
            span = getSpan(spans, row, column)
            column_count = getSpanColumnCount(span)
            if column_count > 1:
                text_row = span[0][0]
                text_column = span[0][1]
                text = table[text_row][text_column]
                length = getLongestLineLength(text)
                end_column = text_column + column_count
                available_space = sum(widths[text_column: end_column])
                available_space += column_count - 1
                while length > available_space:
                    for i in range(text_column, end_column):
                        widths[i] += 1
                        available_space = sum(widths[text_column: end_column])
                        available_space += column_count - 1
                        if length <= available_space:
                            break
    return widths


def convertToSpans(table, spans):
    """Converts all cells to spans"""
    new_spans = []
    for row in range(len(table)):
        for column in range(len(table[row])):
            span = getSpan(spans, row, column)
            if not span:
                new_spans.append([[row, column]])
    new_spans.extend(spans)
    new_spans = list(sorted(new_spans))
    return new_spans


def data2rst(table, spans=[[[0, 0]]], use_headers=True):
    table = addCushions(table)
    spans = sortSpans(spans)
    spans = convertToSpans(table, spans)

    widths = getWidths(table, spans)
    heights = getHeights(table, spans)

    cells = []
    for span in spans:
        cell = makeTextCell(table, span, widths, heights, use_headers)
        cells.append(cell)
    cells = list(sorted(cells))
    output = mergeCells(cells)
    return output

if __name__ == "__main__":

    table = [
        ["Header 1", "Header 2", "Header3", "Header 4"],
        ["row 1, column 1", "column 2", "column 3", "column 4"],
        ["row 2", "Cells span columns.", "", ""],
        ["row 3", "Cells\nspan rows.", "- hi\n- sup?\n- bye", ""],
        ["row 4", "", "", ""]
    ]

    # These are [Row, Column] pairs of merged cells
    span0 = ([2, 1], [2, 2], [2, 3])
    span1 = ([3, 1], [4, 1])
    span2 = ([3, 3], [3, 2], [4, 2], [4, 3])

    my_spans = [span0, span1, span2]

    print(data2rst(table, spans=my_spans, use_headers=True))
