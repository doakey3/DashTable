def truncate_empty_lines(lines):
    """
    Removes all empty lines from above and below the text.

    We can't just use text.strip() because that would remove the leading
    space for the table.

    Parameters
    ----------
    lines : list of str

    Returns
    -------
    lines : list of str
        The text lines without empty lines above or below
    """
    while lines[0].rstrip() == '':
        lines.pop(0)
    while lines[len(lines) - 1].rstrip() == '':
        lines.pop(-1)
    return lines
