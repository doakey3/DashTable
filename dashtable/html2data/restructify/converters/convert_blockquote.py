def convert_blockquote(element, text):
    depth = -1
    while element:
        if (not element.name == '[document]' and
                not element.parent.get('id') == '__RESTRUCTIFY_WRAPPER__'):
            depth += 1
        element = element.parent

    if text:
        lines = text.split('\n')
        for i in range(len(lines)):
            lines[i] = (depth * "    ") + '    ' + lines[i]
            lines[i] = lines[i].rstrip()
        text = '\n'.join(lines)
    return text
