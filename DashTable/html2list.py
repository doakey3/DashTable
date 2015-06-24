"""Give it a html file with only a table inside it, and 
convert it to 3 lists:
one with the data
one with the rowspan_list_list
and the last one with the colspan
"""

from bs4 import BeautifulSoup

def simplify_dictlist(datalist):
    """ lots of useless data for the dashtable.py: we keep only used data inside"""
    my_table = []
    for row in datalist:
        my_table.append([])
        for col in row:
            my_table[-1].append(col['in'])
    return my_table

def html2list(file):
    """ main function """
    soup = BeautifulSoup(open(file))
    table = soup.find('table')
    data_list = []
    rowspan_idx = 1
    colspan_idx = 1

    allrows = table.findAll('tr')
    #########################################################
    # First, create the data list:                          #
    #########################################################
    for idx_row, row in enumerate(allrows):
        data_list.append([])
        allcols = row.findAll('td')
        
        for col in allcols:
            cell_dict = {}
            cell_dict['in'] = col.text.strip()
            cell_dict['rowspan_added'] = False
            cell_dict['colspan_added'] = False
            if col.has_attr('rowspan'):
                cell_dict['rowspan'] = rowspan_idx
                cell_dict['rowspan_nb'] = int(col['rowspan'])
                rowspan_idx += 1
            else:
                cell_dict['rowspan'] = 0
                cell_dict['rowspan_nb'] = 1
                
            if col.has_attr('colspan'):
                cell_dict['colspan'] = colspan_idx
                cell_dict['colspan_nb'] = int(col['colspan'])
                colspan_idx += 1
            else:
                cell_dict['colspan'] = 0
                cell_dict['colspan_nb'] = 1
            data_list[idx_row].append(cell_dict)
    colspan_idx = 1
    rowspan_idx = 1
    ####################################################################################
    # then, deal with the rowspan (first) and colspan (after)..                        #
    ####################################################################################
    # Fist, detect rowspan :
    for idx_row, row in enumerate(data_list):
        for idx_col, col in enumerate(row):
            if col['rowspan'] != 0 and not col['rowspan_added']:
                for cspan_nb in range(col['rowspan_nb']-1): # check whether it's 'rowspan=2' or 'rowspan=3' etc...
                    if col['colspan'] == 0:
                        data_list[idx_row+1+cspan_nb].insert(idx_col, {'in': "", 'rowspan': rowspan_idx, 'rowspan_added': True,\
                                                                    'colspan':0, 'colspan_added':False})
                    else:
                        data_list[idx_row+1+cspan_nb].insert(idx_col, {'in': "", 'rowspan': rowspan_idx, 'rowspan_added': True,\
                                                                    'colspan':col['colspan'], 'colspan_added':True})
                rowspan_idx += 1

    # then, detect colspan
    for idx_row, row in enumerate(data_list):
        for idx_col, col in enumerate(row):
            # Case: it's a colspan AND the cell wasn't added during the rowspan phase:
            if col['colspan'] != 0 and not col['colspan_added']:
                for cspan_nb in range(col['colspan_nb']-1): # we modify the number of cells specified in the html colspan=XX
                    # Modify the Data_list :
                    try: # we're trying because maybe the cell already exist (created during rowspan phase):
                        for rspan_nb in range(col['rowspan_nb']):
                            data_list[idx_row+rspan_nb].insert(idx_col+1, {'in': "", 'colspan': colspan_idx, 'colspan_added': True,\
                                                              'rowspan': col['rowspan'], 'rowspan_added': False})
                    except:
                        data_list[idx_row+rspan_nb].append({'in': "", 'colspan': colspan_idx, 'colspan_added': True,\
                                                              'rowspan': rowspan_idx, 'rowspan_added': False})
                colspan_idx += 1

    #####################################################################################################
    #    Creating the colspan and rowspan from the datalist (now that it has the correct list number
    #####################################################################################################
#     print(data_list)
    rowspan_list = []
    colspan_list = []
    for idx_row, row in enumerate(data_list):
        rowspan_list.append([])
        colspan_list.append([])
        for cell in row:
            rowspan_list[-1].append(cell['rowspan'])           
            colspan_list[-1].append(cell['colspan'])
    data_list = simplify_dictlist(data_list)            
    
#     print(data_list)
#     print("rowspan ={}".format(rowspan_list))
#     print("colspan ={}".format(colspan_list))
    return (data_list, rowspan_list, colspan_list)

if __name__ == "__main__":
#     html2list("test_files/simple_input.html")
#     html2list("test_files/colspan_input.html")
    html2list("test_files/rowspan_input.html")
#     html2list("test_files/colspanANDrowspan_input.html")