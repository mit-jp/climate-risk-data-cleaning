'''All data is refenerences by ordering, not by the names themseves, to bypass discrepencies in the naming.
This script checks to see the differences between two dataframes and allows the user to analyze the differences and decide
what to do about them.'''

# input the table, index to compare in the table, the index of the reference dataframe, and which ordering
def fix(tbl, tblix, refix, choice):
    import pandas as pd
    tblout = tbl
    # decide which ordering
    ref = pd.read_csv(r'Parsed Data/ID match.csv')
    if choice == 2:
        ref = pd.read_csv(r'Parsed data/ID match resorted.csv')
    elif choice == 3:
        ref = pd.read_csv(r'Parsed data/County no id.csv')
    i = 0
    while i < ref.shape[0]:
        if refix == 1:
            #check the differences between the given values
            if int(ref.iat[i, refix]) != (tblout.iat[i, tblix]):
                print('Discrepency found at ' + str(i) +'\nValue is ' + str(ref.iat[i, refix]) + ' in reference table and ' + str(tblout.iat[i, tblix]) + ' in current table')
                prompt = 'Type \'1\' to add an empty row in table, \'2\' to delete row, and \'3\' to ignore \n'
                x = input(prompt)
                # add an empty row
                if x == '1':
                    tblout = pd.concat([tblout[0:i], pd.DataFrame([], index=[i]), tblout[i:]])
                # delte a row
                elif x == '2':
                    tblout = pd.concat([tblout[0:i], tblout[i+1:]])
                    #tblout = tblout[0:i].append([tblout[i+1:tblout.shape[0]]])
                    i -= 1
                # do nothing
            i += 1
        else:
            if ref.iat[i, refix] != (tblout.iat[i, tblix]):
                print('Discrepency found at ' + str(i) +'\nValue is ' + str(ref.iat[i, refix]) + ' in reference table and ' + str(tblout.iat[i, tblix]) + ' in current table')
                prompt = 'Type \'1\' to add an empty row in table, \'2\' to delete row, and \'3\' to ignore \n'
                x = input(prompt)
                if x == '1':
                    tblout = pd.concat([tblout[0:i], pd.DataFrame([], index=[i]), tblout[i:]])
                elif x == '2':
                    tblout = pd.concat([tblout[0:i], tblout[i+1:]])
                    #tblout = tblout[0:i].append([tblout[i+1:tblout.shape[0]]])
                    i -= 1
            i += 1
    return tblout