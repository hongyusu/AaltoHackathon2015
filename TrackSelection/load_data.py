import pandas as pd
import numpy as np

################
# Normalize workout data
################

def load(path):
    workout_df = pd.read_csv(path, sep=' ', 
                             quotechar='\'', 
                             names=['file_name', 'lat', 'lng', 'workout_type', 
                                    'user_id', 'distance_raw', 'datetime', 'average_speed', 'max_speed', 'calorie', 'cities_raw'],
                             parse_dates = [6])

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

    return workout_df
