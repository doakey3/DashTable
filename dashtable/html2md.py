import os
from .html2data import html2data
from .data2md import data2md


def html2md(html_string):
    """
    Convert a string or html file to a markdown table string.

    Parameters
    ----------
    html_string : str
        Either the html string, or the filepath to the html

    Returns
    -------
    str
        The html table converted to a Markdown table

    Notes
    -----
    This function requires BeautifulSoup_ to work.

    Example
    -------
    >>> html_text = '''
    ... <table>
    ...     <tr>
    ...         <th>
    ...             Header 1
    ...         </th>
    ...         <th>
    ...             Header 2
    ...         </th>
    ...         <th>
    ...             Header 3
    ...         </th>
    ...     <tr>
    ...         <td>
    ...             <p>This is a paragraph</p>
    ...         </td>
    ...         <td>
    ...             Just text
    ...         </td>
    ...         <td>
    ...             Hot dog
    ...         </td>
    ...     </tr>
    ... </table>
    ... '''
    >>> import dashtable
    >>> print(dashtable.html2md(html_text))
    |      Header 1       | Header 2  | Header 3 |
    |---------------------|-----------|----------|
    | This is a paragraph | Just text | Hot dog  |

    .. _BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
    """

    if os.path.isfile(html_string):
        file = open(html_string, 'r', encoding='utf-8')
        lines = file.readlines()
        file.close()
        html_string = ''.join(lines)

    table_data, spans, use_headers = html2data(html_string)
    if table_data == '':
        return ''

    return data2md(table_data)
