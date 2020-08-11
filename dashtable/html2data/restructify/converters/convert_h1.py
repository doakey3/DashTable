from wcwidth import wcswidth


def convert_h1(element, text):
    """
    Add '=' to the bottom of text
    """
    if text:
        text = text + '\n' + '=' * wcswidth(text)
    return text
