## Data Cleaning Steps

# Dependencies
import pandas as pd
import json
import sys
import IPython

# read csv data and convert to pandas dataframe
df = pd.read_csv("Tornadoes_SPC_1950to2015.csv")

# create location column
df['location'] = df[['slat', 'slon']].apply(tuple, axis=1)

# Filter data to years 2010 and newer
new_df = df.loc[df.yr >= 2010, :]

# Select columns to keep
df1 = new_df[[
'yr',
'date',
'st',
'mag',
'inj',
'fat',
'loss',
'closs',
'len',
'wid',
'slat',
'slon',
'location']]
df1.head()

# reset index
df1.reset_index(inplace = True, drop = True)

# Add state full names
data = {'StName':['Alabama',
'Alaska',
'Arizona',
'Arkansas',
'California',
'Colorado',
'Connecticut',
'Delaware',
'Florida',
'Georgia',
'Hawaii',
'Idaho',
'Illinois',
'Indiana',
'Iowa',
'Kansas',
'Kentucky',
'Louisiana',
'Maine',
'Maryland',
'Massachusetts',
'Michigan',
'Minnesota',
'Mississippi',
'Missouri',
'Montana',
'Nebraska',
'Nevada',
'New Hampshire',
'New Jersey',
'New Mexico',
'New York',
'North Carolina',
'North Dakota',
'Ohio',
'Oklahoma',
'Oregon',
'Pennsylvania',
'Rhode Island',
'South Carolina',
'South Dakota',
'Tennessee',
'Texas',
'Utah',
'Vermont',
'Virginia',
'Washington',
'West Virginia',
'Wisconsin',
'Wyoming']}

df = pd.DataFrame(data)
cw_location = 'http://app02.clerk.org/menu/ccis/Help/CCIS%20Codes/'
cw_filename = 'state_codes.html'

states = pd.read_html(cw_location + cw_filename)[0]
state_code_map = dict(zip(states['Description'], 
                          states['Code']))
df['StAbbr'] = df['StName'].map(state_code_map)
code_state_map = dict(zip(states['Code'],
                          states['Description']))
df['StNameAgain'] = df['StAbbr'].map(code_state_map)
df = df.rename(columns={'stName': 'State_Name', 'StAbbr': 'st'})

new_df2 = pd.merge(df1, df, on='st', how='left')
df3 = new_df2[[
'yr',
'date',
'st',
'StName',
'mag',
'inj',
'fat',
'loss',
'closs',
'len',
'wid',
'slat',
'slon',
'location']]

# Convert to geoJSON format

def df_to_geojson(df3, properties, lat='slat', lon='slon'):
    # create a new python dict to contain our geojson data, using geojson format
    geojson = {'type':'FeatureCollection', 'features':[]}
    # loop through each row in the dataframe and convert each row to geojson format
    for _, row in df3.iterrows():
        # create a feature template to fill in
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        # fill in the coordinates
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        # for each column, get the value and add it as a new feature property
        for prop in properties:
            feature['properties'][prop] = row[prop]
        # add this feature (aka, converted dataframe row) to the list of features inside our dict
        geojson['features'].append(feature)
    return geojson

cols = [
'yr',
'date',
'st',
'StName',
'mag',
'inj',
'fat',
'loss',
'closs',
'len',
'wid',
'slat',
'slon',
'location'
]
geojson = df_to_geojson(df3, cols)

IPython.display.display({'application/geo+json': geojson}, raw=True)

# Note - final variable name to import is "geojson"
