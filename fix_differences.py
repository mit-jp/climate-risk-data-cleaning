def fix(tbl, tblix, refix):
    import pandas as pd
    tblout = tbl
    ref = pd.read_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/Cypress Output Python/Copy of name_ID_match.csv')
    i = 0
    while i < ref.shape[0]:
        if refix == 1:
            if int(ref.iat[i, refix]) != (tblout.iat[i, tblix]):
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