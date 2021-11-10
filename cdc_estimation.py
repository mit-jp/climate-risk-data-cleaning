''' Create a hashmap of the different regional groupings by state FIPS'''
import us

def create_regional_hashmap():
    # Put all states into regions, dictionary of lists
    regional_groupings = {
        'northeast': ['Maine', 'New Hampshire', 'Vermont', 'Massachusetts', 'Rhode Island', 'Connecticut', 'New York',
                      'New Jersey', 'Pennsylvania'],
        'midwest': ['Ohio', 'Indiana', 'Illinois', 'Michigan', 'Wisconsin', 'Minnesota', 'Iowa', 'Missouri',
                    'North Dakota',
                    'South Dakota', 'Nebraska', 'Kansas'],
        'south': ['Delaware', 'Maryland', 'District of Columbia', 'Virginia', 'West Virginia', 'North Carolina',
                  'South Carolina', 'Georgia', 'Florida', 'Kentucky', 'Tennessee', 'Alabama', 'Mississippi', 'Arkansas',
                  'Louisiana', 'Oklahoma', 'Texas'],
        'west': ['Montana', 'Idaho', 'Wyoming', 'Colorado', 'New Mexico', 'Arizona', 'Utah', 'Nevada', 'Washington',
                 'Oregon', 'California', 'Alaska', 'Hawaii']}

    # Replace state names with state codes
    for k in regional_groupings.keys():  # loop through all keys
        i = 0
        for i in range(len(regional_groupings[k])):  # loop through all the values
            state = regional_groupings[k][i].lower()
            regional_groupings[k][i] = int(us.states.lookup(state).fips)  # replace by fips code
    return regional_groupings