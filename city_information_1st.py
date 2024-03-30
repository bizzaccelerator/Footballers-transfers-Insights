import requests
from bs4 import BeautifulSoup as bs
import urllib3
import json
import pandas as pd
from datetime import datetime
import os, os.path
from pathlib import Path

# Identifying the cities to work with
today = datetime.now().date()
day_name = today.strftime("%A")
number_day = today.strftime("%d")
month_name = today.strftime("%b")
month_number = today.strftime("%m")
year = today.strftime("%Y")

# Obtaining the data from current day
# input_file = f'C://Users/jober/OneDrive/Desktop/Footballers_transfers_Insights/data/players_data/{year}/{month_number}_{month_name}/{year}_{month_name}_{number_day}_{day_name}.csv'
input_file = 'C://Users/jober/OneDrive/Desktop/Footballers_transfers_Insights/data/players_data/2024/03_Mar/2024_Mar_29_Friday.csv'
dates = pd.read_csv(input_file,sep=",")

# reading a complete day
equipos = dates[dates['team_left']!="Without ClubWithout Club"]
equipos = pd.Series(equipos['team_left']).reset_index(drop=True)

# Consulting teams' information from wikipedia by
# 1st. defining the parameters of the API
search_query = equipos
language_code = 'es'
number_of_results = 1
with open('C://Users/jober/webscraper/city_data/wiki_credentials.json') as user_file: # Calling the secret wiki-credentials
  file_contents = json.load(user_file)
Access_token = file_contents['Access_token']
headers = {
    'Authorization': Access_token,
    'User-Agent': 'reader (jobert.gutierrez@gmail.com)'
}
# 2nd. Consulting the API to locate the articles about the teams
articles = []
for team in search_query:
    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': team, 'limit': number_of_results}
    response = requests.get(url, headers=headers, params=parameters)
    articles.append(json.loads(response.text))

# 3rd. Extracting the urls of every team found
team_urls = list()
for page in articles:
  for item in page['pages']:
    display_title = item['title']
    article_url = 'https://' + language_code + '.wikipedia.org/wiki/' + item['key']
    team_urls.append(article_url)

# 4rd. Actually consulting every article to get the information of the teams
teams_data = list()
for url in team_urls:
    http = urllib3.PoolManager()
    html = http.request("GET",f'{url}')  # Extract the returned information in a variable
    soup = bs(html.data.decode('utf-8'),'html.parser')      # Parsing the information
    
    try:
        # Extracting the relevant parts
        labels = soup.find("table", {'class':'infobox'}).find_all("th",attrs={"style":"text-align:left;font-size: 92%; width: 36%;;"})
        infos = soup.find("table", {'class':'infobox'}).find_all("td",attrs={"style":"font-size: 92%;;"})

        # Preparing the dictionary keys
        data_keys = list()
        [data_keys.append(label.text) for label in labels]
            
        # Preparing the dictionary values
        data_values = list()
        [data_values.append(info.get_text(strip=True)) for info in infos]

        # Building the dictionary
        dict_team = dict()
        for key in data_keys:
            for value in data_values:
                dict_team[key] = value,
                data_values.remove(value)
                break

        teams_data.append(dict_team)
    except:
        teams_data.append({})

# Building a dictionary from the data found for today
from collections import defaultdict
info_compiled = defaultdict(list)

# Compilator of dictionaries:
no_data = ('No data',)
if len(teams_data) == 0:

    info_compiled['Nombre'].append(no_data)
    info_compiled['Apodo(s)'].append(no_data)
    info_compiled['Fundación'].append(no_data)
    info_compiled['Presidente'].append(no_data)
    info_compiled['Entrenador'].append(no_data)
    info_compiled['Estadio'].append(no_data)
    info_compiled['Ubicación'].append(no_data)
    info_compiled['Capacidad'].append(no_data)

else:
    for d in teams_data: # you can list as many input dicts as you want here
        position = teams_data.index(d)
        if 'Nombre' in d.keys():
            if position == 0:
                for key, value in d.items():
                    info_compiled[key].append(value)
            else:
                for key, value in d.items():
                    if key in info_compiled:
                        info_compiled[key].append(value)
                    else:
                        lenght = len(info_compiled['Nombre'])-1
                        i = 1
                        while i <= lenght:
                            info_compiled[key].append(no_data)
                            if i == lenght:
                                info_compiled[key].append(value)
                                break
                            i = i + 1
                total_keys = set(info_compiled.keys())
                current_keys = set(d.keys())
                for key in total_keys.difference(current_keys):
                    info_compiled[key].append(no_data)
        else:
            total_keys = set(info_compiled.keys())
            for key in total_keys:
                info_compiled[key].append(no_data)

# Building a row dataframe with all the information found for the teams
df = pd.DataFrame.from_dict(info_compiled)

# Curating information in the row dataframe
df = df[['Nombre', 'Apodo(s)', 'Fundación', 'Presidente','Entrenador', 
       'Estadio', 'Ubicación', 'Capacidad']]

# Preparing the final df for export
df['Nombre'] = df['Nombre'].str[0]
df['Apodo(s)'] = df['Apodo(s)'].str[0]
df['Fundación'] = df['Fundación'].str[0]
# df['Propietario(s)'] = df['Propietario(s)'].str[0]
df['Presidente'] = df['Presidente'].str[0]
df['Entrenador'] = df['Entrenador'].str[0]
df['Estadio'] = df['Estadio'].str[0]
df['Ubicación'] = df['Ubicación'].str[0]
df['Capacidad'] = df['Capacidad'].str[0]
# df['Inauguración'] = df['Inauguración'].str[0]
# df['Mánager'] = df['Mánager'].str[0]
# df['Liga'] = df['Liga'].str[0]

# Updating the new columns
df['city'] = df['Ubicación'].str.split(",")
df['name_reported']=equipos

# Identifying the final city column
df['city'] = df['city'].str[0]


# To get the data in a new file, we prepare the file name
today = datetime.now().date()
day_name = today.strftime("%A")
number_day = today.strftime("%d")
month_name = today.strftime("%b")
month_number = today.strftime("%m")
year = today.strftime("%Y")
dataset_file = f'cities_info_{year}_{month_name}_{number_day}_{day_name}'
# dataset_file2 = f'cities_series_{year}_{month_name}_{number_day}_{day_name}'

# Creates a directory if doesn't exist in windows
# outdir = Path(f"./city_data/{year}/{month_number}_{month_name}")
outdir = Path(f"./data/city_data/{year}/03_Mar")
if not os.path.exists(outdir):
    os.makedirs(outdir)
outname = Path(f"{dataset_file}.csv")
# outname2 = Path(f"{dataset_file2}.csv")
fullpath = os.path.join(outdir, outname)
# fullpath2 = os.path.join(outdir, outname2)

# Save the new dataset in the directory selected
df.to_csv(fullpath,index=False)

# ciudades = pd.Series(df['city']).reset_index(drop=True)
# ciudades.to_csv(fullpath2,index=False)
