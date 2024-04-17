import io
import pandas as pd
from pandas import DataFrame
import requests
import json
import numpy as np
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data_from_api(data: DataFrame, *args, **kwargs):

    # extracting the locations only
    def select_number_columns(data):
        cities = data[['city']]
        return cities

    locations = select_number_columns(data)

    # reading the geographic information of the cities in that day
    limit_results= "2"
    with open("/home/src/default_repo/open_weather_API.json") as user_file:
        file_contents = json.load(user_file)
    Access_token = file_contents['key']

    city_data = list()
    for index,row in locations.iterrows():
        base_url = 'http://api.openweathermap.org/geo/1.0/'
        endpoint = 'direct'
        limit= limit_results
        API_key = Access_token
        try:
            if row['city'] == 'No data':
                city_data.append({})
            else:
                response = requests.get(base_url + endpoint + f"?q={row['city']}&limit={limit}&appid={API_key}", params = {})
                city_data.append(response.json()[0])
        except:
            city_data.append({})

    # Building a currated dictionary from the cities information
    city_list = list()
    for item in city_data:
        try:
            cities = {
                'name' : item['name'],
                'latitude' : item['lat'],
                'longitude' : item['lon'],
                'state': item['state'],
                'country' : item['country'],
                }
            city_list.append(cities)
        except:
            cities = {
                'name' : "No data",
                'latitude' : np.nan,
                'longitude' : np.nan,
                'state': "No data",
                'country' : "No data",
                }
            city_list.append(cities)
    
    # opening the list
    # places = pd.DataFrame(city_list)
    # def select_number_columns(places):
    #     cities = places[['name']]
    #     return cities
    # places = pd.DataFrame(select_number_columns(places))
    
    # Consulting the weather information for the geo-located cities of that day
    weather_data = list()
    for item in city_list:
        if item['name']=='No data':
            weather_data.append({})
        else:
            base_url = 'https://api.openweathermap.org/data/2.5/'
            endpoint = 'weather'
            lat = item['latitude']
            lon = item['longitude']
            response = requests.get(base_url + endpoint + f'?lat={lat}&lon={lon}&exclude=hourly&appid={API_key}', params = {})
            weather_data.append(response.json())

    # Preparing to futher utilization
    block_var1 = kwargs['configuration'].get('block_var1')
    block_var2 = kwargs['configuration'].get('block_var2')

    return {"variable1":city_list, "variable2": weather_data}
