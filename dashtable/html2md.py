try:
    from .html2data import html2data
    from .data2md import data2md

except SystemError:
    from html2data import html2data
    from data2md import data2md

import os
import argparse


def html2md(html_string):
    """
    Convert a string or html file to a markdown table string
    """

    if os.path.isfile(html_string):
        file = open(html_string, 'r')
        lines = file.readlines()
        file.close()
        html_string = ''.join(lines)

    table_data, spans, use_headers = html2data(html_string)
    if table_data == '':
        return ''

    return data2md(table_data)


def cmdline():
    """
    Use command line to convert an input html file to markdown file
    example: python html2md.py input.html output.md
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to input html file")
    parser.add_argument("output_file", help="path to output file")
    args = parser.parse_args()

    file = open(args.input_file, 'r')
    lines = file.readlines()
    file.close()
    html_string = ''.join(lines)

    output_string = html2md(html_string)

    file = open(args.output_file, 'w')
    file.write(output_string)
    file.close()
