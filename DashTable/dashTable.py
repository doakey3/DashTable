def create_widthwithzero(width, colspan_list):
    """ helper function for function table_list_to_ascii().
    for ex.: colspan_list = [[0,0,0,0,0,0], [0,1,1,2,2,0]]
    it will create widthwithzero = [[3,3,2,4,5,2],[3,6,0, 10,0,2]]
    it's used to calculate what is the cell in the same column in the row before or after.
    If we use the original width:  [[3,3,2,4,5,2],[3,6,10,2]], there's a problem of
    correspondence between indexes of different rows."""
    widthwithzero = []
    for row_idx, row in enumerate(colspan_list):
        offset = 0
        previouscell = 0
        widthwithzero.append([])
        for col_idx, col in enumerate(row):
            if col == 0:
                widthwithzero[-1].append(width[row_idx][col_idx+offset])
            if col != 0 and previouscell != col:
                widthwithzero[-1].append(width[row_idx][col_idx+offset])
            if col != 0 and previouscell == col:
                widthwithzero[-1].append(0)
                offset -= 1
            previouscell = col
    return widthwithzero            
            
def colspan_converter(table, colspan_list, width):
    """modify the width when there's colspan
    Until now, we have ignored all colspan cell for the calculation of the
    width"""
    len_mergedcells = 0 # the width of the colspan cells which are merged
    len_adjacentcells = 0 # the width of the cells in the adjacent rows of the merged cell row
    offset = 0 # it's used because we'll delete item in table and columnsizematrix
    # their indexes will become out of sync with colspan indexes.
    """ colspan list: [ [0, 0, 0, 0],
                      [0, 1, 1, 0]
                      [0, 0, 0, 1]]
      we're using currentcolspan_nb to store the current colspan
      if matrix is [0,1,1,0], it must delete not the first element but the others."""
    for row_idx, row in enumerate(colspan_list):
        # at the beginning of each row processing, reset to default previouscolspan_nb
        # and offset
        previouscolspan_nb = 0
        offset = 0
        """ the Loop inside the colspan_list = [[0,0,0,0,0],[0,1,1,2,2,0]]"""
        for cell_idx, cell in enumerate(row):
            """4 cases depending on if current cell different of previouscell and 
                                    if previous cell is 0 or not"""
            # * Case 1: current cell different from previous one AND previous one = 0
            # --> it's index '1' in [0, 1, 1, 2, 2]: add the new merged cell for the calculation, no popped cell"""
            if cell != previouscolspan_nb and previouscolspan_nb == 0:
                """ table = [[aa, bbb, cc, d],
                             [eee, ff, '', gggg]
                             [hh, iiii, jj, k]]
                * len_mergedcells = the cells which are colspan: we add their length
                * len_adjacentcells = the 'original cells (i.e cells without colspan), as 
                calculated with the width initially which have passed systematically
                when it was colspan. we add their length"""
                # the lengths must be reset to default (not an addition like in Case 4)
                len_mergedcells = len(table[row_idx][cell_idx+offset])
                len_adjacentcells = width[row_idx][cell_idx+offset]
                
            # * Case 2: current cell different from previous one AND previous one != 0
            # --> it's index '3' in [0, 1, 1, 2, 2]: 2 Steps : Resize the Matrix THEN 
            #                                 add the new merged cell for the calculation, no popped cell"""
            elif cell != previouscolspan_nb and previouscolspan_nb != 0:
                """ it's only *now* that we can determine the size of the colspan cell (we know it's
                now finished)"""
                if len_adjacentcells > len_mergedcells: 
                    """for ex.: [[aa, bbb, ccc, dd],
                                 [eee, ffff, ggg],
                                 [hhh, iii, jj, kkk]] where ffff spans 2 columns (1 and 2)
                    bbb + ccc > ffff (where 'ffff' is the colspan cell
                    So : we use the adjacent cells lengths: length of 'ffff' becomes that of 'bbb'+'ccc'+1
                    '+1*(-offset)' because it's minus a '|' in the merged cells compared to adjacent cells
                    (and it's proportional to the number of cols the cell is spanning)"""
                    # the merged cell are smaller than the adjacent cell in other row
                    # index is '-1' because it's about the cell where the colspan is
                    width[row_idx][cell_idx-1+offset] = len_adjacentcells + 1*(-offset) 
                else: # the merged cell are bigger than other adjacent cell rows:
                    """for ex.: [[aa, bb, cc, dd],
                                 [eee, fffff, ggg],
                                 [hhh, i, jj, kkk]]
                    fffff > bb+cc (where 'fffff' is the colspan cell
                    So : we use the colspan cell length to change all the 'normal' cells adjacent: 
                    length of cc and jj becomes as such that length of bb+cc= length of 'fffff'
                                                                       i+jj =                  """
                    for i in range(len(width)):
                        if i == row_idx: # the row where the colspan is
                            # index is '-2' because it's about the cell where the colspan is
                            width[i][cell_idx-2+offset] = len_mergedcells
                            # index is '-1' because it's about the cell where the colspan is
                        else: # the other rows ('-1' because of the absence of '|' in merged cell) :
                            width[i][cell_idx-1+offset] += len_mergedcells - len_adjacentcells -1 
                
                """and then we add the merged cell for the new colspan (idem case 1)"""
                # the lengths must be reset to default (not an addition like in Case 4)
                len_mergedcells = len(table[row_idx][cell_idx+offset])
                len_adjacentcells = width[row_idx][cell_idx+offset]
            
            # * Case 3: current cell identical from previous one AND previous one = 0
            # --> it's index '1' in [0, 0, 1, 1, 2, 2]: do nothing 
            elif cell == previouscolspan_nb and previouscolspan_nb == 0:
                pass
            
            # * Case 4: current cell identical from previous one AND previous one != 0
            # --> it's index '3' in [0, 0, 1, 1, 2, 2]: add the adjacent cell for calculation add pop the cell 
            elif cell == previouscolspan_nb and previouscolspan_nb != 0:
                # delete the cell:
                table[row_idx].pop(cell_idx+offset) 
                """ table = [[aa, bbb, cc, d],
                             [eee, ff, gggg]
                             [hh, iiii, jj, k]]
                * popped cell = '' 
                we've checked it's not the first colspan, without it, we could have deleted 'ff'!"""
                popped_cell = width[row_idx].pop(cell_idx+offset)
                len_adjacentcells += popped_cell
                # update the offset because we delete items in width and table
                offset -= 1
                
            # at each end of for loop (i.e. end of processing each cell), we actualize the previouscolspan_nb
            previouscolspan_nb = cell

def create_separator(row_index, width, widthwithzero, rowspan_list, colspan_list, lastsep=False):
    """calculate the separator for the *next* row: take the row number, look what the width is, 
    and give back the 'sep' special problem: if there's colspan, the '+' dispappear: 
    not recognized by ReST. solution: try to find the row BEFORE (and not AFTER) where there is no colspan
    for ex.: +-----+-------+------+------+
             |  aa |   bb  |  cc  |  hhh |
             +-----+--------------+------+  Not good!
             |  dd |     dddd     |  ii  |
             +-----+--------------+------+
    lastsep is an option: when doing: (problem with the last sep when the row before is rowspan)
             +-----+-------+------+------+
             |  aa |   bb  |  cc  |  hhh |
             +     +-------+------+------+  Not good!
             |  dd |  dddd |  ee  |  ii  |
             +     +-------+------+------+
    """
    sep = ""
    # it 's the first row: always display the next row (always no problem for the first row)
    if row_index == 0:
        for col in width[row_index]:
            sep += "+" + col*'-'
        return sep + '+\n'
    # not the first row
    else:
        """using the above ex.: 
        width = [[ 2, 2, 2, 3],
                             [ 2, 4,    3]]"""
        # using an offset because the column size matrix where there's 
        # colspan is shorter from the colspan list (same thing than with colspan_converter
        for idx_col, col in enumerate(colspan_list[row_index]):
            """we're using a dashORspace: place holder for '-' or ' ' (useful for table with colspan AND rowspan associated)"""
            """ First, we deal with rowspan :"""
            # check whether the row can have rowspan:
            # its rowspan!= 0 and it's the same number. It must not be  
            if rowspan_list[row_index][idx_col] != 0 and \
                rowspan_list[row_index][idx_col] == rowspan_list[row_index -1][idx_col] and \
                not lastsep:
                dashORspace = ' '
#                 sep += "+" + ' '*width[row_index][idx_col]
            else:
                dashORspace = '-'
            
            """then with colspan:"""
            # No colspan, we use the row after:
            if col == 0:
                sep += '+' + dashORspace*widthwithzero[row_index][idx_col]
            # It's a colspan: different cases :
            else:
                # it's the first row: we use the row after:
                if row_index == 0: # take the row after to have the correct separator
                    if width[row_index][idx_col] == 0: # the width is 0
                        pass
                    else:
                        sep += '+' + dashORspace*widthwithzero[row_index][idx_col]
            # we deal at first with the case of the width is 0: use the row before:
            #           +----+-----+-----+
            #           |aa  |bbbb |ccccc|
            #           +----+-----+-----+
            #           |dddd|ee         |
            #           +----+-----------+
                elif widthwithzero[row_index][idx_col] == 0: 
                    if dashORspace == ' ':
                        pass
                    else:
                        sep += '+' + dashORspace*widthwithzero[row_index-1][idx_col]
                # case where the width of the cell is <= of the cell the row before: we can use the cell of the row after
                elif widthwithzero[row_index][idx_col] <= widthwithzero[row_index-1][idx_col]: 
                    sep += '+' + dashORspace*widthwithzero[row_index][idx_col]
                # case where the width of the cell is bigger than ones of the row before: use the row before:
                else: 
                    sep += '+' + dashORspace*widthwithzero[row_index-1][idx_col]
    return sep + '+\n'

def print_row(row_index, column_size, table, rowspan_list):
    """print each row: that'is: | X | X | X| (not the row of the list...)"""
    result_f = ""
    remainder = []
    for col_index, cell in enumerate(table[row_index]):
        # keep only the first element of the string, before the line return
        try:
            first_cut, second_cut = cell.split('\n', 1)
        except:
            first_cut = cell
            second_cut = '' # no extra \n in the cell
        # if remainder exist, is in rowspan_list and it's not the last row, put it into the table's next row:
        if rowspan_list[row_index][col_index] != 0 and row_index != len(table)-1 and second_cut != '':
            table[row_index+1][col_index] += second_cut
        else:
            remainder.append(second_cut)
        result_f += "{:{width}}".format(first_cut, width=column_size[col_index]) + "|"
    return (result_f, remainder)

def check_not_empty(lst):
    """check if a list contains only empty elements (used for the extra row
    added when there's '\n" inside a cell)
    """
    for i in lst:
        if i:
            return True
    return False

def table_list_to_ascii(table, rowspan_list, colspan_list):
    """main function"""
    # determine the biggest cell in each column.
    column_size = []
    column = []
    
    ##################################################################
    #  Calculating the width without the colspan cells               #
    #  and taking account of the '\n' if it exists                   #
    ##################################################################
    # using a copy of the table (because we'll delete the colspan cells):
    table_copy = []
    # it's a deep copy: i.e copy the lists inside the list
    for row in table:
        table_copy.append([])
        for cell in row:
            table_copy[-1].append(cell)

    # convert the row in columns.
    for line in zip(*table_copy):
        column.append(list(line))
    # When the cell contains '\n', it's split in cells:
    for col in column:
        max_cell = 0
        for cell in col:
            if len(max(cell.split('\n'), key=len)) > max_cell:
                max_cell = len(max(cell.split('\n'), key=len))
        column_size.append(max_cell)
#         column_size.append(len(max(line, key=len)))
    width = [list(column_size) for i in table_copy] # don't forget to use a COPY of the list!
    
    ##################################################################
    #  Calculating the width with the colspan cells      #
    #                                                                #
    ##################################################################
    # convert the column size if there's colspan in the table:
    colspan_converter(table, colspan_list, width)
    """using a width with zero: for ex.: [[3,3,2,4,5,2][3,6,0,10,0,2]]"""
    widthwithzero = create_widthwithzero(width, colspan_list)

    ##################################################################
    #  Printing the table...                                         #
    #                                                                #
    ##################################################################
    # Print a return before the table (easier to create a test...)
    result = "\n" 

    for row_idx, row in enumerate(table):
        # create separator:
        result += create_separator(row_idx, width, widthwithzero, rowspan_list, colspan_list)

        result += "|" 
        # keep only the first element of the string, before the line return
        result_f, remainder = print_row(row_idx, width[row_idx], table, rowspan_list)
        result += result_f
        row = remainder
        table_row = [row]
        # print extra row if there's '\n' inside 
        while check_not_empty(row):
            result_f, remainder = print_row(0, width[row_idx], table_row, rowspan_list)
            result += "\n|" + result_f 
            row = remainder
            table_row = [row]
        result += "\n" 
    # last row, print the sep: using the "lastsep=True" option!
    result += create_separator(len(table) -1, width, widthwithzero, rowspan_list, colspan_list, lastsep=True)
                                
    return result

if __name__ == "__main__":
    # Usage example
#     """test_simple(self):"""
#     table = [
#      ['aaaa', 'bbbbb', 'ccc', 'dddddd'],
#      ['eeeee','fff', 'dddddd', 'eee'],
#      ['gg','hhhhhhhh', 'i', 'jjj'],
#      ['kkk', 'lllll', 'mm', 'nnnnnnnnn']
#      ]
#     colspan_list = [
#            [0, 0, 0, 0],
#            [0, 0, 0, 0],
#            [0, 0, 0, 0],
#            [0, 0, 0, 0]
#            ]
#     rowspan_list = [
#            [0, 0, 0, 0],
#            [0, 0, 0, 0],
#            [0, 0, 0, 0],
#            [0, 0, 0, 0]
#            ]
#     result = table_list_to_ascii(table, colspan_list, rowspan_list)
#     print(result)
#  
#     """test_carriage_return(self):"""
#     table = [
#      ['aaaa', 'bbbbbbbb', 'ccc\nccc\ncccccccc', 'ddddddd'],
#      ['eeeeeee','ffffff', 'gggg', 'hhhhhh'],
#      ['iiiii','jjjjj', 'kkkkk', 'lllllll'],
#      ['mm \nmmmm', 'nnnnn', 'ooo', 'pppppp']
#      ]
#     colspan_list = [
#            [0, 0, 0, 0],
#            [0, 0, 0, 0],
#            [0, 0, 0, 0],
#            [0, 0, 0, 0]
#            ]
#     rowspan_list = [
#            [0, 0, 0, 0],
#            [0, 0, 0, 0],
#            [0, 0, 0, 0],
#            [0, 0, 0, 0]
#            ]
#     result = table_list_to_ascii(table, colspan_list, rowspan_list)
#     print(result)
# 
# 
#     """test_colspan_simple(self):"""
#     table = [
#          ['aaa', 'bbbb', 'ccc', 'dddd'],
#          ['eeeee','fffff', 'gggg', 'hhh'],
#          ['iiiii','jjjjjjjjj', '', 'kkkkk'],
#          ['ll', 'mmmm', 'nn', 'oooo']
#          ]
#     colspan_list = [
#            [0, 0, 0, 0],
#            [0, 0, 0, 0],
#            [0, 1, 1, 0],
#            [0, 0, 0, 0]
#            ]
#     rowspan_list = [
#            [0, 0, 0, 0],
#            [0, 0, 0, 0],
#            [0, 0, 0, 0],
#            [0, 0, 0, 0]
#            ]
# 
#     """test_rowspan_simple(self):"""
#     table = [
#          ['aaa', 'bbbbb', 'ccc', 'ddddddd'],
#          ['eeeeee','fffff', 'ggggggg', 'hhhh'],
#          ['iiii','jjjj', 'kkkk', ''],
#          ['lllll', 'mmm', 'nn', 'oooooo']
#          ]
#     colspan_list = [
#            [0, 0, 0, 0],
#            [0, 0, 0, 0],
#            [0, 0, 0, 0],
#            [0, 0, 0, 0]
#            ]
#     rowspan_list = [
#            [0, 0, 0, 0],
#            [0, 0, 0, 1],
#            [0, 0, 0, 1],
#            [0, 0, 0, 0]
#            ]
#     result = table_list_to_ascii(table, colspan_list, rowspan_list)
#     print(result)
#     
#     """test_colspan_with_colspan_nb"""
#     table = [
#              ['aa', 'bbb', 'ccc', 'dd', 'eee', 'jj'], 
#              ['ff', 'gggg', '', 'hh', '', 'lllll'] 
#              ]
#     rowspan_list = [[0, 0, 0, 0, 0, 0], 
#                     [0, 0, 0, 0, 0, 0]
# #                     , [0, 0, 0, 0, 0]
#                     ]
#     colspan_list = [[0, 0, 0, 0, 0, 0], 
#                     [0, 1, 1, 2, 2, 0] 
# #                     ,[0, 0, 0, 0, 0]
#                     ]
# 
#     """test_rowspan_with rowspan_nb"""
#     table = [
#              ['aa', 'bbb', 'ccc'], 
#              ['dd', '', 'ee'],
#              ['ff', 'gggg', 'hhhh'],
#              ['iiii','','jj'],
#              ['k','ll','mm']
#              ]
#     rowspan_list = [[0, 1, 0], 
#                     [0, 1, 0],
#                     [0, 2, 0],
#                     [0, 2, 0],
#                     [0, 0, 0],
#                     ]
#     colspan_list = [[0, 0, 0], 
#                     [0, 0, 0],
#                     [0, 0, 0],
#                     [0, 0, 0],

#     """test_colspan_spanning_several_cols"""
#     table = [
#              ['aa', 'bbb', 'ccc', 'dd', 'eee', 'jj'], 
#              ['ff', 'gggg', '', '', '', 'lllll'] 
#              ]
#     rowspan_list = [[0, 0, 0, 0, 0, 0], 
#                     [0, 0, 0, 0, 0, 0]
# #                     , [0, 0, 0, 0, 0]
#                     ]
#     colspan_list = [[0, 0, 0, 0, 0, 0], 
#                     [0, 1, 1, 1, 1, 0] 
# #                     ,[0, 0, 0, 0, 0]
#                     ]
 
#     """test_rowspan_spanning_several_rows"""
#     table = [
#              ['aa', 'bbb', 'ccc'], 
#              ['dd', '', 'ee'],
#              ['xx', '', 'yyy'],
#              ['ff', 'gggg', 'hhhh'],
#              ['iiii','','jj'],
#              ['','ll','mm']
#              ]
#     rowspan_list = [[0, 1, 0], 
#                     [0, 1, 0],
#                     [0, 1, 0],
#                     [0, 2, 0],
#                     [3, 2, 0],
#                     [3, 0, 0],
#                     ]
#     colspan_list = [[0, 0, 0], 
#                     [0, 0, 0],
#                     [0, 0, 0],
#                     [0, 0, 0],
#                     [0, 0, 0],
#                     [0, 0, 0]]

#     """test_rowspan_AND_colspan_THE_ULTIMATE_TEST"""
#     table = [
#              ['aa', 'bbb', 'cc', 'zzzzzz'], 
#              ['dd', 'ee', '', 'nnn'],
#              ['xx', '', '', 'ooooo'],
#              ['ff', 'gggg', 'h', 'ss'],
#              ['iiii','r','jj', 'tttttt'],
#              ['k','ll','mm', 'uuu']
#              ]
#     rowspan_list = [
#                     [0, 0, 0, 0], 
#                     [0, 1, 1, 0],
#                     [0, 1, 1, 0],
#                     [0, 0, 0, 0],
#                     [0, 0, 0, 0],
#                     [0, 0, 0, 0]
#                     ]
#     colspan_list = [
#                     [0, 0, 0, 0], 
#                     [0, 1, 1, 0],
#                     [0, 1, 1, 0],
#                     [0, 0, 0, 0],
#                     [0, 0, 0, 0],
#                     [0, 0, 0, 0]
#                     ]
    
    """ colspan and rowspan, mixed"""
    table = [['aaaa', 'COLSPAN', '', 'ROWSPAN'], ['jj', 'under_COLSPAN1', 'under_COLSPAN2', ''], ['fff', 'kk', 'hhhhh', 'iii']]
    rowspan_list = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]]
    colspan_list = [[0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]] 

    result = table_list_to_ascii(table, rowspan_list, colspan_list)
    print(result)