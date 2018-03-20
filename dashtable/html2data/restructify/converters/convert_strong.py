def convert_strong(element, text):
    """
    Add '**' to both ends of the text

    Parameters
    ----------
    element : bs4.node
    text : str

    Returns
    -------
    str
        bolded text
    """
    if text:
        text = "**%s**" % text

    return text
