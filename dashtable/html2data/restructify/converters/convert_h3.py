def convert_h3(element, text):
    """
    Adds '~' to the bottom of the text
    """
    if text:
        text = text + '\n' + '~' * len(text) + '\n'
    return text
