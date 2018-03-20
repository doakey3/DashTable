def convert_a(element, text):
    if text:
        href = element.get('href')
        classes = dict(element.attrs).get('class', '')
        if 'footnote-reference' in classes:
            text = '[' + href + ']_'
        elif len(text.split(' ')) > 1:
            text = '`' + text + '`_'
        else:
            text = text + '_'
    return text
