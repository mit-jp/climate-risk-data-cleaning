'''This code performs all the operations to format the cdc data downloads to a standard data format. '''


import pandas as pd
import numpy as np

def organize(county_data, state_data, national_data):
    # Import all datasets
    df_county = pd.read_csv(county_data, sep='\t',
                            engine='python')
    df_state = pd.read_csv(state_data, sep='\t', engine='python')
    df_national = pd.read_csv(national_data, sep='\t',
                              engine='python')

    # Organize the data
    # drop unnecessary columns
    df_county = df_county.drop(['Notes', 'Age Group', 'Crude Rate'], axis=1)
    df_state = df_state.drop(['Notes', 'Age Group', 'Crude Rate'], axis=1)
    df_national = df_national.drop(['Notes', 'Age Group', 'Crude Rate'], axis=1)

    # drop rows full of nans
    df_county = df_county.dropna(how='all')
    df_state = df_state.dropna(how='all')
    df_national = df_national.dropna(how='all')

    df_county['State ANSI'] = (df_county['County Code'] / 1000).apply(np.floor)  # extract state code from fpis code
    df_county['County ANSI'] = df_county['County Code'] - (df_county['County Code'] / 1000).apply(
        np.floor) * 1000  # extract county code from fpis code
    df_county = df_county.drop(['County', 'County Code'], axis=1)  # drop county and dounty code rows
    df_state = df_state.drop(['State'], axis=1)

    # Group ages into specified ranges
    df_county = df_county.replace({'Age Group Code': {'1': '0-5', '1-4': '0-5', '5-9': '5-25', '10-14': '5-25',
                                                      '15-19': '5-25', '20-24': '5-25', '25-34': '25+', '35-44': '25+',
                                                      '45-54': '25+', '55-64': '25+', '65-74': '25+', '75-84': '25+',
                                                      '85+': '25+'}})
    df_state = df_state.replace({'Age Group Code': {'1': '0-5', '1-4': '0-5', '5-9': '5-25', '10-14': '5-25',
                                                    '15-19': '5-25', '20-24': '5-25', '25-34': '25+', '35-44': '25+',
                                                    '45-54': '25+', '55-64': '25+', '65-74': '25+', '75-84': '25+',
                                                    '85+': '25+'}})
    df_national = df_national.replace({'Age Group Code': {'1': '0-5', '1-4': '0-5', '5-9': '5-25', '10-14': '5-25',
                                                          '15-19': '5-25', '20-24': '5-25', '25-34': '25+',
                                                          '35-44': '25+', '45-54': '25+', '55-64': '25+',
                                                          '65-74': '25+', '75-84': '25+', '85+': '25+'}})

    # Clean up data and reorder
    # replace 'supprssed' and 'missing' with nans to allow for math operations
    df_county = df_county.replace(
        {'Deaths': {'Suppressed': np.nan, 'Missing': np.nan}, 'Population': {'Suppressed': np.nan, 'Missing': np.nan}})
    df_state = df_state.replace(
        {'Deaths': {'Suppressed': np.nan, 'Missing': np.nan}, 'Population': {'Suppressed': np.nan, 'Missing': np.nan}})

    # set class of deaths and population to float
    df_county['Deaths'] = df_county['Deaths'].astype(float)
    df_county['Population'] = df_county['Population'].astype(float)
    df_state['Deaths'] = df_state['Deaths'].astype(float)

    # sum column values by state, then county, then age group code. needs to be done because multiple values for each combination due to higher granualrity in orginial data
    df_county = df_county.groupby(['State ANSI', 'County ANSI', 'Age Group Code']).sum()
    df_state = df_state.groupby(['State Code', 'Age Group Code']).sum()
    df_national = df_national.groupby(['Age Group Code']).sum()

    # unstack from multiindexing
    df_county = df_county.unstack(level=2)
    df_county.columns = ['_'.join(col) for col in df_county.columns.values]
    df_county = df_county.reset_index()
    df_county = df_county.sort_values(by=['State ANSI', 'County ANSI'])  # resort rows


    df_state = df_state.unstack(level=1)
    df_state.columns = ['_'.join(col) for col in df_state.columns.values]
    df_state = df_state.reset_index()

    # calculate percent deaths for each age group
    df_county['Percent Deaths 0-5'] = df_county['Deaths_0-5'] / df_county['Population_0-5']
    df_county['Percent Deaths 25+'] = df_county['Deaths_25+'] / df_county['Population_25+']
    df_county['Percent Deaths 5-25'] = df_county['Deaths_5-25'] / df_county['Population_5-25']

    return [df_county, df_state, df_national]