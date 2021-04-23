## Data Cleaning Steps

# Dependencies
import pandas as pd
import json
import sys
import IPython
from flask import jsonify

###################################
# function to return top 10 states based on causalty (fatality + injury)
def top10():
    # import csv data and convert to dataframe df
    df = pd.read_csv("data/Tornadoes_SPC_1950to2015.csv")
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
    'slon']]

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
    'slon']]

    # drop rows for Puerto Rico (will be NaN in StName column)
    df3.dropna(subset=["StName"])

    # reset index
    df3.reset_index(inplace = True, drop = True)

    # GROUP BY STEPS
    # group by state name
    df_groups = df3.groupby(['StName']).sum()
    # drop columns
    df_groups = df_groups.drop(columns=['yr','mag','closs','len','wid','slat','slon'])
    # reset index
    df_groups.reset_index(inplace = True, drop = False)
    # create casualty column (sun of injuries and fatalities)
    df_groups["casualty"] = df_groups["inj"] + df_groups["fat"]
    # round casualty to whole number
    df_groups["casualty"].round(0)
    # sort values descending based on casualty
    df_groups = df_groups.sort_values(by="casualty", ascending=False)
    # reset index putting state names as a column
    df_groups.reset_index(inplace = True, drop = True)
    # filter data to top 10 rows
    df_10_states = df_groups.head(10)

    # Extract states and casualty to lists
    states = df_10_states["StName"].tolist()
    casualty = df_10_states["casualty"].tolist()

    #fatality = df_10_states["fat"].tolist()
    #injury = df_10_states["inj"].tolist()

    return jsonify([{
        "x": states,
        "y": casualty,
        "marker": {
            "color": 'rgba(255,153,51,0.6)',
        },
        "text": casualty,
        "textposition": "auto",
        "type": "bar"
    }])