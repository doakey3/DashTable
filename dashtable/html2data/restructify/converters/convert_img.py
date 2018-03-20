def convert_img(element, text):
    src = element.get("src", None)

    if element.parent.name == "[document]" or element.parent.get('id') == '__RESTRUCTIFY_WRAPPER__':
        if src:
            text = '\n.. image:: ' + src

    elif src:
        text = '|' + src + '|'
    return text
