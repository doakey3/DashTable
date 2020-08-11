from wcwidth import wcswidth


def convert_h2(element, text):
    """
    Adds '-' to the bottom of the text
    """
    if text:
        text = text + '\n' + '-' * wcswidth(text)
    return text
