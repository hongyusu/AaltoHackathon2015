# coding: utf-8
import pandas as pd
import numpy as np
from collections import defaultdict
from simplejson import dumps

################
# Normalize workout data
################

workout_df = pd.read_csv('file_first_gps_city.txt', sep=' ', 
                         quotechar='\'', 
                         names=['file_name', 'lat', 'lng', 'workout_type', 
                                'user_id', 'distance_raw', 'cities_raw'])

units = set()
def normalize_raw_disance_string(s):
    """convert '2.5 km|mi' to float values in unit of km"""
    if len(s.split()) < 2:
        return np.nan
    else:
        value, unit = s.split()
        value = float(value)
        if unit == 'mi':
            value *= 1.60934
        return value

distance = workout_df['distance_raw'].apply(normalize_raw_disance_string)


workout_df.insert(5, 'distance', distance)
workout_df.drop('distance_raw', 1, inplace=True)


def normalize_raw_city_string(s):
    if not isinstance(s, float):
        return sorted(s.split("___"))[0] #get the first city in alphabetically order
    else:
        return np.nan

city = workout_df['cities_raw'].apply(normalize_raw_city_string)
workout_df.insert(6, 'city', city)
workout_df.drop('cities_raw', 1, inplace=True)

# from ~54000 to ~18000 items
workout_df = workout_df[pd.notnull(workout_df['city']) & pd.notnull(workout_df['distance'])]



################
# Total distance per city statistics 
################

city_gps_df = pd.read_csv('city_gps_refined.txt', sep='___',  
                          names=['city', 'lat', 'lng']) 
city2loc = {name: (lat, lng)
            for _, name, lat, lng, in city_gps_df.itertuples()}

city_dist = defaultdict(float)
for i,row in workout_df.iterrows():
    city_dist[row['city']] += row['distance']

loc_dist = {}
for city in city_dist:
    loc_dist[city2loc[city]] = city_dist[city]


with open('loc2dist.json', 'w') as f:
    f.write(dumps([(loc[0], loc[1], loc_dist[loc]) for loc in loc_dist]))
