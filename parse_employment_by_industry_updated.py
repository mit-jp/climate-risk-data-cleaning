import pandas as pd
import numpy as np
import fix_differences as diff
#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/CAEMP25N__ALL_AREAS_2001_2019.csv', nrows=105270, low_memory=False)
df = pd.pivot(df, index='GeoName', columns='Description', values=['2019']).reset_index()
print(df)
#state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
#states = [item.lower() for item in state_names]
#df = df[~df['GeoName'].isin(states)]
#df = df[~df['GeoName'].str.contains('united states')]
df['County'] = np.nan
df['State'] = np.nan
df[['County', 'State']] = df['GeoName'].str.rsplit(', ', n=1, expand=True)
df = pd.concat([df.iloc[:, 34:37], df.iloc[:, 33], df.iloc[:, 1:33]], axis=1)
df = df.sort_values(by=['State', 'County'])
df = df.iloc[0:3138, :]
#print(df)
df.to_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/Cypress Output Python/Employment by industry updated.csv', index = False)