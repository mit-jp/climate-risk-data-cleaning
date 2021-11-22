import pandas as pd
import re
import fix_differences as diff
import useful_analysis_functions as fns

# import
df = pd.read_csv(r'Project data/Population.csv')

# remove state rows
df = fns.remove_state_rows(df, 'CTYNAME')

# reformat county names
df = fns.remove_confusing_words(df, 'CTYNAME')

prev_col = df['POPESTIMATE2010']
# calculate percent change from previous year
for col in df.columns: # loop through all columns
    if col != 'CTYNAME' and col != 'POPESTIMATE2010':
        year = re.findall(r'\d+', col)[0] #extract year
        name = 'pctchange' + str(int(year) - 1) + '-' + str(year) # create column name
        df[name] = ((df[col]-prev_col)/prev_col)*100 # calculate percent difference
        prev_col = df[col]
df['AVGPOPCNG2010-2019'] = df.iloc[:, 11:].sum(axis=1, min_count=1)/9 # calculate average percent change

df = diff.fix(df, 0, 0, 3)
df.to_csv(r'Parsed data/Population.csv', index=False)