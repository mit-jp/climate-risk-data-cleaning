from census import Census
from us import states
import pandas

c = Census("f88810dbb816ce76eb26fc06cb5d34c2ea1f96ad")
data = pandas.DataFrame(c.acs5.get(('NAME', 'B01003', 'B09001', 'B02008', 'B17001', 'DP05_0029PE'), {'for': 'county:*'}))
data['state'] = data.apply(lambda row: get_state(row.NAME), axis=1)
data['county'] = data.apply(lambda row: get_county(row.NAME), axis=1)
data = data.sort_values(by=["state", "county"])
del data['NAME']
data.to_csv('/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/demographics.csv')
