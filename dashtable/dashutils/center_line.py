import math

from wcwidth import wcswidth


def center_line(space, line):
    """
    Add leading & trailing space to text to center it within an allowed
    width

    Parameters
    ----------
    space : int
        The maximum character width allowed for the text. If the length
        of text is more than this value, no space will be added.\
    line : str
        The text that will be centered.

    Returns
    -------
    line : str
        The text with the leading space added to it
    """
    line = line.strip()

    left_length = math.floor((space - wcswidth(line)) / 2)
    right_length = math.ceil((space - wcswidth(line)) / 2)

    left_space = " " * int(left_length)
    right_space = " " * int(right_length)

    line = ''.join([left_space, line, right_space])

    return line
