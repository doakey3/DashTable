import os
from .html2data import html2data
from .data2rst import data2rst


def html2rst(html_string, force_headers=False, center_cells=False,
             center_headers=False):
    """
    Convert a string or html file to an rst table string.

    Parameters
    ----------
    html_string : str
        Either the html string, or the filepath to the html
    force_headers : bool
        Make the first row become headers, whether or not they are
        headers in the html file.
    center_cells : bool
        Whether or not to center the contents of the cells
    center_headers : bool
        Whether or not to center the contents of the header cells

    Returns
    -------
    str
        The html table converted to an rst grid table

    Notes
    -----
    This function **requires** BeautifulSoup_ to work.

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
    ...             <ul>
    ...                 <li>List item 1</li>
    ...                 <li>List item 2</li>
    ...             </ul>
    ...         </td>
    ...         <td>
    ...             <ol>
    ...                 <li>Ordered 1</li>
    ...                 <li>Ordered 2</li>
    ...             </ol>
    ...         </td>
    ...     </tr>
    ... </table>
    ... '''
    >>> import dashtable
    >>> print(dashtable.html2rst(html_text))
    +---------------------+----------------+--------------+
    | Header 1            | Header 2       | Header 3     |
    +=====================+================+==============+
    | This is a paragraph | -  List item 1 | #. Ordered 1 |
    |                     | -  List item 2 | #. Ordered 2 |
    +---------------------+----------------+--------------+

    .. _BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
    """

    if os.path.isfile(html_string):
        file = open(html_string, 'r', encoding='utf-8')
        lines = file.readlines()
        file.close()
        html_string = ''.join(lines)

    table_data, spans, use_headers = html2data(
        html_string)

    if table_data == '':
        return ''
    if force_headers:
        use_headers = True

    return data2rst(table_data, spans, use_headers, center_cells, center_headers)
