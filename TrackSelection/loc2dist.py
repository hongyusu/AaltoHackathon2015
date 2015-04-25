# coding: utf-8
import pandas as pd
import numpy as np
from collections import defaultdict
from simplejson import dumps



################
# Total distance per city statistics 
################

workout_df = data.load('file_first_gps_city.txt')

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

print loc_dist
with open('loc2dist.json', 'w') as f:
    f.write(dumps([(loc[0], loc[1], loc_dist[loc]) for loc in loc_dist]))
