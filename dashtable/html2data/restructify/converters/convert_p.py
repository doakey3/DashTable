def convert_p(element, text):
    """
    Adds 2 newlines to the end of text
    """
    depth = -1
    while element:
        if (not element.name == '[document]' and
                not element.parent.get('id') == '__RESTRUCTIFY_WRAPPER__'):
            depth += 1

        element = element.parent

    if text:
        text = '    ' * depth + text
    return text
