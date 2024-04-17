import pandas as pd
from pandas import DataFrame
from datetime import datetime
import numpy as np
from typing import Dict, List
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

@transformer
def transform(data:List, data_raw:List, **kwargs):
    #calling variables passed upstream
    city_list = data['variable1']
    weather_data = data['variable2']

    # Elaborating a curated dictionay with the weather information found
    city_info = list()
    for item in weather_data:
        if len(item) != 0:
            weather = {
                'name' : item['name'],
                'latitude' : item['coord']['lat'],
                'longitude' : item['coord']['lon'],
                'sky_weather' : item['weather'][0]['main'],
                'weather_description' : item['weather'][0]['description'],
                'timestamp': datetime.fromtimestamp(item['dt']),
                'country' : item['sys']['country'],
                }
            city_info.append(weather)
        else:
            print('used this path')
            no_weather = {
                'name' : "No data",
                'latitude' : np.nan,
                'longitude' : np.nan,
                'sky_weather' : "No data",
                'weather_description' : "No data",
                'timestamp': np.nan,
                'country' : "No data",
                }
            city_info.append(no_weather)

    # Merging two dictionaries with geographic and weather information to a single dataframe
    df1 = pd.DataFrame(city_list)
    df2 = pd.DataFrame(city_info)

    cols = ['sky_weather','weather_description','timestamp']
    weather_compiled = df1.merge(df2[cols], left_index=True, right_index=True)
    weather_compiled['name']=data_raw['city']
    weather_compiled['Team']=data_raw['name_reported']

    # return {"variable1":city_list, "variable2": city_info}
    return weather_compiled