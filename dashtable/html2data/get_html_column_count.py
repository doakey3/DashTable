def get_html_column_count(html_string):
    """
    Gets the number of columns in an html table.

    Paramters
    ---------
    html_string : str

    Returns
    -------
    int
        The number of columns in the table
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("ERROR: You must have BeautifulSoup to use html2data")
        return

    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    if not table:
        return 0

    column_counts = []
    trs = table.findAll('tr')
    if len(trs) == 0:
        return 0

    for tr in range(len(trs)):
        if tr == 0:
            tds = trs[tr].findAll('th')
            if len(tds) == 0:
                tds = trs[tr].findAll('td')
        else:
            tds = trs[tr].findAll('td')

        count = 0
        for td in tds:
            if td.has_attr('colspan'):
                count += int(td['colspan'])
            else:
                count += 1

        column_counts.append(count)

    return max(column_counts)
