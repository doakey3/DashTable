from bs4 import BeautifulSoup
from bs4 import NavigableString

from .process_tag import process_tag
from .add_links import add_links


def restructify(html):
    html = '<div id="__RESTRUCTIFY_WRAPPER__">' + html + '</div>'
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find() == None:
        return str(soup)

    root = soup.find()
    text = process_tag(root)
    converted_text = text

    converted_text = converted_text.rstrip() + '\n\n'

    converted_text = add_links(converted_text, html).rstrip()

    while len(converted_text.split('\n\n\n')) > 1:
        split = converted_text.split('\n\n\n')
        converted_text = '\n\n'.join(split)

    converted_text += '\n\n'

    used_srcs = []
    images = soup.find_all('img')
    for img in images:
        src = img.get("src", None)
        if (not img.parent == '[document]' and
                not img.parent.get('id') == "__RESTRUCTIFY_WRAPPER__" and
                src and
                not src in used_srcs):
            converted_text += '|' + src + '| image:: ' + src + '\n'
            used_srcs.append(src)

    return converted_text.strip()
