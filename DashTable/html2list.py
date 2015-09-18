"""Give it a html file with only a table inside it, and 
convert it to 3 lists:
one with the data
one with the rowspan_list_list
and the last one with the colspan
"""

from bs4 import BeautifulSoup


def already_exists(idx_row, idx_col, row):
    """ helper for html2list main.
    check in the row of the datalist if an element with the given idx already exists. """
    for element in row:
        if element['idx'][0] == idx_row and element['idx'][1] == idx_col:
            return True

def html2list(file):
    """ main function """
    # we can input a file but even a string!
    if file.rsplit('.', 1)[-1] == "html":
        soup = BeautifulSoup(open(file), 'html.parser')
    else:
        soup = BeautifulSoup(file, 'html.parser') # the 'file' is actually a string probably
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
    # then, deal with the rowspan and colspan (simultaneously)..                        #
    ####################################################################################
    # we use another list where the span will be correct (and index are in the dict)
    span_datalist = []
    curr_idx_row = -1 # because the list begins at -1! 
    for idx_row, row in enumerate(data_list):
        curr_idx_row += 1 
        curr_idx_col = -1 # because the list begins at -1! 
        for idx_col, col in enumerate(row):
            curr_idx_col += 1

            # loop to check if the index already exists (created with rowspan)
            already_exist_token = True
            while already_exist_token:
                if already_exists(curr_idx_row, curr_idx_col, span_datalist):
                    curr_idx_col +=1
                else:
                    already_exist_token = False
                

            # Then we check for the rowspan and colspan (or both)
            # *special case* : it's a colspan AND rowspan cell:
            if col['rowspan'] != 0 and col['colspan'] != 0:
                # update the rowspan_idx field in the initial cell:
                span_datalist.append({'in':col['in'], 'idx':[curr_idx_row, curr_idx_col],\
                                  'colspan_idx':colspan_idx, 'rowspan_idx':rowspan_idx})
                row_to_change = col['rowspan_nb'] # the nb of row that the colspan must be applied to
                for rspan_nb in range(col['rowspan_nb']-1): # check whether it's 'rowspan=2' or 'rowspan=3' etc...
                    span_datalist.append({'in': "", 'idx':[curr_idx_row+1+rspan_nb, curr_idx_col],\
                                          'rowspan_idx': rowspan_idx, 'colspan_idx': colspan_idx})
                alt_curr_idx_col = curr_idx_col
                for row_to_change in range(col['rowspan_nb']):# the nb of row that the colspan must be applied to
                    for cspan_nb in range(col['colspan_nb']-1): # we modify the number of cells specified in the html colspan=XX
                        span_datalist.append({'in': "", 'idx':[curr_idx_row+row_to_change, curr_idx_col+1+cspan_nb], \
                                              'colspan_idx': colspan_idx, 'rowspan_idx':rowspan_idx})
                        if row_to_change == 0: # don't increase when the colspan loop is adding new col on other rows.
                            alt_curr_idx_col += 1 # the idx is increased since a cell was added
                curr_idx_col = alt_curr_idx_col
                colspan_idx += 1
                rowspan_idx += 1

            # is it a rowspan cell?
            elif col['rowspan'] != 0:
                # update the rowspan_idx field in the initial cell:
                span_datalist.append({'in':col['in'], 'idx':[curr_idx_row, curr_idx_col],\
                                  'colspan_idx':0, 'rowspan_idx':rowspan_idx})
                for rspan_nb in range(col['rowspan_nb']-1): # check whether it's 'rowspan=2' or 'rowspan=3' etc...
                    span_datalist.append({'in': "", 'idx':[curr_idx_row+1+rspan_nb, curr_idx_col],\
                                          'rowspan_idx': rowspan_idx, 'colspan_idx':0})
                rowspan_idx += 1
            #it's a colspan cell
            elif col['colspan'] != 0:
                # update the rowspan_idx field in the initial cell:
                span_datalist.append({'in':col['in'], 'idx':[curr_idx_row, curr_idx_col],\
                                  'colspan_idx':colspan_idx, 'rowspan_idx':0})
                for cspan_nb in range(col['colspan_nb']-1): # we modify the number of cells specified in the html colspan=XX
                    span_datalist.append({'in': "", 'idx':[curr_idx_row, curr_idx_col+1+cspan_nb], \
                                          'colspan_idx': colspan_idx, 'rowspan_idx':0})
                    curr_idx_col += 1 # the idx is increased since a cell was added
                colspan_idx += 1
            # 'normal' case:
            else:
                span_datalist.append({'in':col['in'], 'idx':[curr_idx_row, curr_idx_col],\
                                  'colspan_idx':0, 'rowspan_idx':0})
                

    span_datalist = sorted(span_datalist, key=lambda k: k['idx']) 
    # creating datalist, rowspan_list and colspan_list:
    datalist = []
    colspan_list = []
    rowspan_list = []
    idx_row = -1 # list begins at 0!
    for element in span_datalist:
        if idx_row != element['idx'][0]: # add a new row
            datalist.append([])
            colspan_list.append([])
            rowspan_list.append([])
            idx_row += 1
        datalist[-1].append(element['in'])
        rowspan_list[-1].append(element['rowspan_idx'])
        colspan_list[-1].append(element['colspan_idx'])
    return(datalist, rowspan_list, colspan_list)

if __name__ == "__main__":
#     result = html2list("../test_files/simple_input.html")
#     result = html2list("../test_files/colspan_input.html")
#     result = html2list("../test_files/rowspan_input.html")
#     result = html2list("../test_files/simplerowspan_input.html")
#     result = html2list("../test_files/colspanANDrowspan_input.html")
    result = html2list("../test_files/colspanANDrowspan2.html")
    for i in result:
        print(i)
    