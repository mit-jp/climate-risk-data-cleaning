import pandas as pd
import re
import fix_differences as diff
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
df = pd.read_csv(r'Project data/Population.csv')
df['CTYNAME'] = df['CTYNAME'].str.lower()
state_names = ['Alaska', 'Alabama', 'Arkansas', 'American Samoa', 'Arizona', 'California', 'Colorado', 'Connecticut', 'District of Columbia', 'Delaware', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Iowa', 'Idaho', 'Illinois', 'Indiana', 'Kansas', 'Kentucky', 'Louisiana', 'Massachusetts', 'Maryland', 'Maine', 'Michigan', 'Minnesota', 'Missouri', 'Mississippi', 'Montana', 'North Carolina', 'North Dakota', 'Nebraska', 'New Hampshire', 'New Jersey', 'New Mexico', 'Nevada', 'New York', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Virginia', 'Virgin Islands', 'Vermont', 'Washington', 'Wisconsin', 'West Virginia', 'Wyoming']
state_names = [x.lower() for x in state_names]
df = df[~df['CTYNAME'].isin(state_names)]
#df = df[df['CTYNAME'].str.contains(' county')]
'''for i in range(len(df)):
    if df.ix[i].str.contains(' county'):
        df.iloc[0, i].str.replace(' county', df.iloc[0, index])
    else:
        index = i'''
df['CTYNAME'] = df['CTYNAME'].str.replace(' county', '')
df['CTYNAME'] = df['CTYNAME'].str.replace(' city and', '')
df['CTYNAME'] = df['CTYNAME'].str.replace(' borough', '')
df['CTYNAME'] = df['CTYNAME'].str.replace(' municipality', '')
df['CTYNAME'] = df['CTYNAME'].str.replace(' census area', '')
df['CTYNAME'] = df['CTYNAME'].str.replace(' parish', '')
df['CTYNAME'] = df['CTYNAME'].str.replace(' city', '')
prev_col = df['POPESTIMATE2010']
for col in df.columns:
    if col != 'CTYNAME' and col != 'POPESTIMATE2010':
        year = re.findall(r'\d+', col)[0]
        name = 'pctchange' + str(int(year) - 1) + '-' + str(year)
        df[name] = df[col]/prev_col
        prev_col = df[col]
print(df)
df = diff.fix(df, 0, 0, 3)
df.to_csv(r'Parsed data/Population.csv', index=False)