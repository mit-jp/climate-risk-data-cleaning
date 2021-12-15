import pandas as pd
import fix_differences as diff
# pd.set_option('display.max_rows', None)
df = pd.read_csv(r'Project data/WildfireRiskToCommunities_County_Summary_2020-03-31.csv') #replace with name/file path of new file
df = df.drop(['STATE', 'COUNTYNS', 'GEOID', 'NAME', 'NAMELSAD'], axis=1)
df = diff.fix(df, 1, 1, 1) #checks difference compared to refece, prompt will tell you what to do
df.to_csv(r'Parsed data/Wildfire Risk.csv', index=False) #rename with final file name