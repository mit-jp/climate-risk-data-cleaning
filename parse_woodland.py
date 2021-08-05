import pandas as pd
import fix_differences as diff
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv(r'Project data/Copy of NASS_Census_Woodland_2017.csv') #replace with name/file path of new file
df = df.sort_values(by=['State ANSI', 'County ANSI']) #sort by state, then county codes, change only if column names are different
df = diff.fix(df, 1, 1, 1) #checks difference compared to refece, prompt will tell you what to do
df.to_csv(r'Parsed data/NASS Cropland.csv', index=False) #rename with final file name