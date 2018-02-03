from bs4 import BeautifulSoup
from .process_tag import process_tag


def add_links(converted_text, html):
    """
    Add the links to the bottom of the text
    """
    soup = BeautifulSoup(html, 'html.parser')

    link_exceptions = [
        'footnote-reference',
        'fn-backref',
        'citation-reference'
    ]

    footnotes = {}
    citations = {}
    backrefs = {}

    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        text = process_tag(link)
        classes = dict(link.attrs).get('class', '')

        if 'footnote-reference' in classes:
            footnotes[href] = '#' + link.get('id')

        elif 'citation-reference' in classes:
            text = process_tag(link)
            citations[text] = '#' + link.get('id')

        elif 'fn-backref' in classes:
            sibling = link.findNext('td')
            text = process_tag(sibling)
            backrefs[href] = text

        excepted_link = False
        for class_type in classes:
            if class_type in link_exceptions:
                excepted_link = True

        if not excepted_link:
            if text.endswith('_'):
                text = text[0:-1]
            if len(text.split(' ')) > 1:
                text = text[1:-1]
            converted_text += '.. _' + text + ': ' + href + '\n'

    if len(footnotes.keys()) > 0:
        converted_text += '\n'

    for key in footnotes.keys():
        text = backrefs[footnotes[key]]
        converted_text += '.. [' + key + '] ' + text + '\n'

    if len(citations.keys()) > 0:
        converted_text += '\n'

    for key in citations.keys():
        text = backrefs[citations[key]]
        converted_text += '.. ' + key[0:-1] + ' ' + text + '\n'

    return converted_text.rstrip()
