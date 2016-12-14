try:
    from .html2data import html2data
    from .data2rst import data2rst

except SystemError:
    from html2data import html2data
    from data2rst import data2rst

import os
import argparse


def html2rst(html_string, force_headers=False):
    """
    Convert a string or html file to an rst table string
    """

    if os.path.isfile(html_string):
        file = open(html_string, 'r')
        lines = file.readlines()
        file.close()
        html_string = ''.join(lines)

    table_data, spans, use_headers = html2data(html_string)
    if table_data == '':
        return ''
    if force_headers:
        use_headers = True

    return data2rst(table_data, spans, use_headers)


def cmdline():
    """
    Use command line to convert an input html file to rst file
    example: python html2rst.py input.html output.rst
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to input html file")
    parser.add_argument("output_file", help="path to output file")
    parser.add_argument("--force_headers", help="Force output to use headers",
                        action="store_true")
    args = parser.parse_args()

    file = open(args.input_file, 'r')
    lines = file.readlines()
    file.close()
    html_string = ''.join(lines)

    output_string = html2rst(html_string, force_headers=args.force_headers)

    file = open(args.output_file, 'w')
    file.write(output_string)
    file.close()
