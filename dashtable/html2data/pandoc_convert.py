import os
import subprocess
import tempfile


def pandoc_convert(text):
    """
    Use pandoc to convert html text to rst

    Parameters
    ----------
    text : str

    Returns
    -------
    str
        converted html text
    """
    tmp = tempfile.NamedTemporaryFile(
            mode='r+b', prefix='offset_', suffix='.html')
    html = tmp.name
    tmp.close()

    tmp = tempfile.NamedTemporaryFile(
            mode='r+b', prefix='offset_', suffix='.rst')
    rst = tmp.name
    tmp.close()

    with open(html, 'w') as f:
        f.write(text)

    subprocess.call([
        'pandoc',
        html,
        '-o', rst
    ])

    with open(rst, 'r') as f:
        rst_text = f.read()

    os.remove(html)
    os.remove(rst)

    return rst_text

