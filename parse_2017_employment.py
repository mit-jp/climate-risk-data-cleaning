import pandas as pd
import fix_differences as diff
df = pd.read_csv(r'Project data/2017 employment.csv')
df = df[:3141]
df = diff.fix(df, 1, 1, 1)
df.to_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/Cypress Output Python/2017 employment.csv', index = False)
