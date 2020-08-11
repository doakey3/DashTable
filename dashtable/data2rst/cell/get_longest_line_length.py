from wcwidth import wcswidth


def get_longest_line_length(text):
    """Get the length longest line in a paragraph"""
    lines = text.split("\n")
    length = 0

    for i in range(len(lines)):
        if wcswidth(lines[i]) > length:
            length = wcswidth(lines[i])

    return length
