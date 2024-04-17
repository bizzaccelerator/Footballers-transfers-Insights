import io
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup as bs
import urllib3
from pandas import DataFrame
from typing import List, Dict
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data_from_api(team_left: DataFrame, *args, **kwargs)-> List[Dict]:

    # Consulting teams' information from wikipedia by
    # 1st. defining the parameters of the API
    search_query = team_left
    language_code = 'es'
    number_of_results = 1
    with open('/home/src/default_repo/wiki_credentials.json') as user_file: # Calling the secret wiki-credentials
        file_contents = json.load(user_file)
    Access_token = file_contents['Access_token']
    headers = {
        'Authorization': Access_token,
        'User-Agent': 'reader (jobert.gutierrez@gmail.com)'
    }
    # 2nd. Consulting the API to locate the articles about the teams
    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    
    articles = list()
    for index,row in search_query.iterrows():
        # print("Requesting data for:", row['team_left'])
        parameters = {'q': row['team_left'], 'limit': number_of_results}
        response = requests.get(url, headers=headers, params=parameters)
        if response.status_code == 200:
            articles.append(json.loads(response.text))
            #print(json.loads(response.text))
        else:
            print(f"Error for user {row['team_left']}")


    # 3rd. Extracting the urls of every team found
    team_urls = list()
    for page in articles:
        for item in page['pages']:
            # print('Requesting information for: ',item['title'])
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

    # team_urls = pd.DataFrame(team_urls)
    
    return [teams_data]