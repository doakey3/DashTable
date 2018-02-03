def convert_div(element, text):
    classes = dict(element.attrs).get('class', '')

    if 'line' in classes:
        depth = -2
        while element:
            if (not element.name == '[document]' and
                    not element.parent.get('id') == '__RESTRUCTIFY_WRAPPER__'):
                depth += 1

            element = element.parent

        if text:
            text = '    ' * depth + '| ' + text

    return text.rstrip()
