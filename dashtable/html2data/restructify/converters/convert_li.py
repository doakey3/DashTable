def get_bullet_depth(element):
    depth = -1
    while element:
        if (not element.name in ['li', '[document]'] and
                not element.parent.get('id') == '__RESTRUCTIFY_WRAPPER__'):
            depth += 1

        element = element.parent

    return depth


def convert_li(element, text):
    parent = element.parent
    if parent is not None and parent.name == "ol":
        index = parent.index(element)

        children = parent.find_all('li', recursive=False)
        space = len(str(len(children))) + 1

        for i in range(len(children)):
            if parent.index(children[i]) == index:
                number = str(i + 1)
                interspace = (space - len(number)) * ' '
                text = number + '.' + interspace + text

        depth = get_bullet_depth(element)

        pre_space = depth * 2 * " "
        text = pre_space + text

    else:
        depth = get_bullet_depth(element)

        bullets = "*-+"
        bullet = bullets[depth % 4 % len(bullets)]

        pre_space = depth * 2 * " "

        if text:
            text = pre_space + bullet + ' ' + text

        if parent.index(element) == 1:
            text = '\n' + text

    return text
