import pandas as pd
import us

df_ac = pd.read_csv(r'Parsed data/All Cause Mortality.csv')

i = 0
count = 0
for i in range(df_ac.shape[0]):
    if (df_ac.iloc[i, 2] > .1) or (df_ac.iloc[i, 2] > .1) or (df_ac.iloc[i, 4] > .1):
        print(df_ac.iloc[i, :])
        count += 1

print(count)



