import pandas as pd
import numpy as np
import fix_differences as diff
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
df = pd.read_csv(r'Project data/Population per square mile.csv')
df['Area_name'] = df['Area_name'].str.lower()
df = df.iloc[1:, :]
# remove state rows 
state_names = ['Alaska', 'Alabama', 'Arkansas', 'American Samoa', 'Arizona', 'California', 'Colorado', 'Connecticut', 'District of Columbia', 'Delaware', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Iowa', 'Idaho', 'Illinois', 'Indiana', 'Kansas', 'Kentucky', 'Louisiana', 'Massachusetts', 'Maryland', 'Maine', 'Michigan', 'Minnesota', 'Missouri', 'Mississippi', 'Montana', 'North Carolina', 'North Dakota', 'Nebraska', 'New Hampshire', 'New Jersey', 'New Mexico', 'Nevada', 'New York', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Virginia', 'Virgin Islands', 'Vermont', 'Washington', 'Wisconsin', 'West Virginia', 'Wyoming']
state_names = [x.lower() for x in state_names]
df = df[~df['Area_name'].isin(state_names)]
df['Area_name'] = df['Area_name'].str.replace('\,[^,]*$', '')
df = diff.fix(df, 0, 0, 3)
df = df.replace(-66666, np.nan)
df.to_csv(r'Parsed data/Population density.csv', index=False)