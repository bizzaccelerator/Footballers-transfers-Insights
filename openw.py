import requests
import pandas as pd
from datetime import datetime
import os, os.path
from pathlib import Path
import json

# Identifying the cities to work with
today = datetime.now().date()
day_name = today.strftime("%A")
number_day = today.strftime("%d")
month_name = today.strftime("%b")
month_number = today.strftime("%m")
year = today.strftime("%Y")


# input_file = f'C://Users/jober/webscraper/city_data/{year}/{month_number}_{month_name}/cities_series{year}_{month_name}_{number_day}_{day_name}.csv'

# extract = pd.read_csv(input_file,sep=",")

# extract.head(2)


# Input test
input_file = 'C://Users/jober/webscraper/city_data/2024/01_Jan/cities_info_2024_Jan_31_Wednesday.csv'
extract = pd.read_csv(input_file,sep=",")

# Extracting the cities in a specific day
locations = pd.Series(extract['city'] ).reset_index(drop=True)

# reading the geographic information of the cities in that day
limit_results= "2"
with open("C://Users/jober/webscraper/weather_api/open_weather_API.json") as user_file:
  file_contents = json.load(user_file)
Access_token = file_contents['key']

city_data = list()
for city_name in locations:
    base_url = 'http://api.openweathermap.org/geo/1.0/'
    endpoint = 'direct'
    limit= limit_results
    API_key = Access_token
    try:
        if city_name == 'No data':
            city_data.append({})
        else:
            response = requests.get(base_url + endpoint + f'?q={city_name}&limit={limit}&appid={API_key}', params = {})
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
            'latitude' : "No data",
            'longitude' : "No data",
            'state': "No data",
            'country' : "No data",
            }
        city_list.append(cities)

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

# Elaborating a curated dictionay with the weather information found
city_info = list()
for item in weather_data:
    try:
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
    except:
        no_weather = {
            'name' : "No data",
            'latitude' : "No data",
            'longitude' : "No data",
            'sky_weather' : "No data",
            'weather_description' : "No data",
            'timestamp': "No data",
            'country' : "No data",
            }
        city_info.append(no_weather)


# Merging two dictionaries with geographic and weather information to a single dataframe
df1 = pd.DataFrame(city_list)
df2 = pd.DataFrame(city_info)


cols = ['sky_weather','weather_description','timestamp']
weather_compiled = df1.merge(df2[cols], left_index=True, right_index=True)
weather_compiled['name']=extract['city']
weather_compiled['Team']=extract['name_reported']

# To get the data in a new file, we prepare the file name
weather_file = f'weather_{year}_{month_name}_{number_day}_{day_name}'

# Creates a directory if doesn't exist in windows

outdir = Path(f"./weather_api/data/{year}/01_Jan")
# outdir = Path(f"./weather_api/data/{year}/{month_number}_{month_name}")
if not os.path.exists(outdir):
    os.makedirs(outdir)
outname = Path(f"{weather_file}.csv")
fullpath = os.path.join(outdir, outname)

# Save the new dataset in the directory selected
weather_compiled.to_csv(fullpath,index=False)

