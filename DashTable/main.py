""" Program to convert an html file (example: input.html) with a table inside it
    to an ASCII table.
    Caveats: take into consideration the spans: rowspan and columnspan
"""
try:
    from . import dashTable
    from . import html2list
except SystemError:
    import dashTable
    import html2list

def main(file_path):
    # get the table
    datalist, rowspan_list, colspan_list = html2list.html2list(file_path)
    #  result = table_list_to_ascii(table, colspan_list, rowspan_list)
    result = dashTable.table_list_to_ascii(datalist, rowspan_list, colspan_list)
    return result

def cmdline():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('input_file', action='store', help='The HTML file to convert')
    opts = parser.parse_args()
    print(main(opts.input_file))

if __name__ == "__main__":
    cmdline()

#     print(main("../test_files/simple_input.html"))
#     print(main("../test_files/colspan_input.html"))
#     print(main("../test_files/rowspan_input.html"))
#     print(main("../test_files/simplerowspan_input.html"))
#     print(main("../test_files/colspanANDrowspan_input.html"))
#     print(main("../test_files/colspanANDrowspan2.html"))