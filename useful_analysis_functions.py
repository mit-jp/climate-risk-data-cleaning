import pandas as pd
import numpy as np

''' Takes in a dataframe and returns a new dataframe that has new columns as a percent of the total of previous columns. Start_index is the
index of the column you would like so sum on.'''
def percent_of_total(df, start_index):
    cols = df.columns.tolist() # create list of column names
    cols_pct = [i + ' pct' for i in cols] # create a new list of percent columns
    sum = df.iloc[:, start_index:].sum(axis=1, min_count=1)
    print(sum)
    for i in range(start_index, len(cols)): # for all the specified columns
        df[str(cols_pct[i])] = df[str(cols[i])] / sum # divide column value by total
    # all operations done on all rows
    return df


def split_county_state_names(df, split_string, table_length, column_name):
    df['County'] = np.nan
    df['State'] = np.nan
    df[['County', 'State']] = df[column_name].str.rsplit(split_string, n=1, expand=True)
    df = df.drop(column_name, axis=1)
    df = pd.concat([df.iloc[:, table_length:table_length+3], df.iloc[:, 0:table_length]], axis=1)
    return df

def remove_confusing_words(df, column_name):
    df[column_name] = df[column_name].str.lower()
    df[column_name] = df[column_name].str.replace(' county', '')
    df[column_name] = df[column_name].str.replace(' city and', '')
    df[column_name] = df[column_name].str.replace(' borough', '')
    df[column_name] = df[column_name].str.replace(' municipality', '')
    df[column_name] = df[column_name].str.replace(' census area', '')
    df[column_name] = df[column_name].str.replace(' parish', '')
    df[column_name] = df[column_name].str.replace(' city', '')
    return df

def switch_two_rows(df, row_1, row_2):
    df1 = df.copy()
    i = 0
    for i in range(len(row_1)):
        df1.iloc[row_1[i], :], df1.iloc[row_2[i], :] = df.iloc[row_2[i], :], df1.iloc[row_1[i], :]
    df = df1
    del (df1)
    return df

def remove_state_rows(df, ref_column):
    df[ref_column] = df[ref_column].str.lower()
    state_names = ['Alaska', 'Alabama', 'Arkansas', 'American Samoa', 'Arizona', 'California', 'Colorado',
                   'Connecticut', 'District of Columbia', 'Delaware', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Iowa',
                   'Idaho', 'Illinois', 'Indiana', 'Kansas', 'Kentucky', 'Louisiana', 'Massachusetts', 'Maryland',
                   'Maine', 'Michigan', 'Minnesota', 'Missouri', 'Mississippi', 'Montana', 'North Carolina',
                   'North Dakota', 'Nebraska', 'New Hampshire', 'New Jersey', 'New Mexico', 'Nevada', 'New York',
                   'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina',
                   'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Virginia', 'Virgin Islands', 'Vermont', 'Washington',
                   'Wisconsin', 'West Virginia', 'Wyoming']
    state_names = [x.lower() for x in state_names]
    df = df[~df[ref_column].isin(state_names)]
    return df

def split_state_and_county_codes(df, column_name):
    df['State ANSI'] = (df[column_name] / 1000).apply(np.floor)
    df['County ANSI'] = df[column_name] - (df[column_name] / 1000).apply(np.floor) * 1000
    df = df.sort_values(by=['State ANSI', 'County ANSI'])  # sort by state then county
    return df

#pd.set_option('display.max_columns', None)