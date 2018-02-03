from bs4 import NavigableString

from .converters import *

def truncate_empties(lines):
    while lines[0].rstrip() == '':
        lines.pop(0)
    while lines[len(lines) - 1].rstrip() == '':
        lines.pop(-1)
    return lines


def process_tag(node):
    """
    Recursively go through a tag's children, converting them, then
    convert the tag itself.

    """
    text = ''

    exceptions = ['table']

    for element in node.children:
        if isinstance(element, NavigableString):
            text += element
        elif not node.name in exceptions:
            text += process_tag(element)

    try:
        convert_fn = globals()["convert_%s" % node.name.lower()]
        text = convert_fn(node, text)

    except KeyError:
        pass

    return text
