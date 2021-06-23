import pandas as pd
import fix_differences as diff
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/CAEMP25N__ALL_AREAS_2001_2019.csv', nrows=3142, low_memory=False)
df = df.transpose()
#df1 = df.iloc[0:3, 0:33]
i = 0
for i in range(0, 3142, 33):
    df = df.append(df.iloc[2, i:i+1], ignore_index=True)

print(df)
df.to_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/Cypress Output Python/Employment by industry updated.csv', index = False)