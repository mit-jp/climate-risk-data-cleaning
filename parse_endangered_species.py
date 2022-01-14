import pandas as pd
import fix_differences as diff
# pd.set_option('display.max_rows', None)
df = pd.read_csv(r'Project data/endangered species.csv') #replace with name/file path of new file
df = df.dropna(how='any')

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")

Latitude = "25.594095"
Longitude = "85.137566"

location = geolocator.reverse(Latitude + "," + Longitude)

df = df.assign(County='')


i = 0
for i in range(df.shape[0]):
    location = geolocator.reverse(str(df.iloc[i,8]) + "," + str(df.iloc[i,9]))
    #print(location)
    address = location.raw['address']
    df.iloc[i, 10] = address['county']

#df.to_csv(r'Parsed data/Endangered Species.csv', index=False) #rename with final file name