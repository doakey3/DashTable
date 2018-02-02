def headers_present(html_string):
    """
    Checks if the html table contains headers and returns True/False

    Parameters
    ----------
    html_string : str

    Returns
    -------
    bool
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("ERROR: You must have BeautifulSoup to use html2data")
        return

    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    if not table:
        return False

    th = table.findAll('th')
    if len(th) > 0:
        return True
    else:
        return False
