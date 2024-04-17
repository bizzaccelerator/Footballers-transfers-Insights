import pandas as pd
from pandas import DataFrame
from typing import List
from collections import defaultdict
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

@transformer
def transform(teams_data: List, team_left, **kwargs):
    
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

    df = pd.DataFrame(info_compiled)

    # Curating information in the row dataframe
    if 'Ubicación' not in df.columns:
        cols = ['Nombre', 'Apodo(s)', 'Fundación', 'Presidente','Entrenador', 
            'Estadio', 'Capacidad']
    else:
        cols = ['Nombre', 'Apodo(s)', 'Fundación', 'Presidente','Entrenador', 
            'Estadio', 'Ubicación', 'Capacidad']

    # Updating the columns
    df = df[cols]

    # Preparing the final df for export
    df['Nombre'] = df['Nombre'].str[0]
    df['Apodo(s)'] = df['Apodo(s)'].str[0]
    df['Fundación'] = df['Fundación'].str[0]
    # df['Propietario(s)'] = df['Propietario(s)'].str[0]
    df['Presidente'] = df['Presidente'].str[0]
    df['Entrenador'] = df['Entrenador'].str[0]
    df['Estadio'] = df['Estadio'].str[0]
    # df['Ubicación'] = df['Ubicación'].str[0]
    df['Capacidad'] = df['Capacidad'].str[0]
    # df['Inauguración'] = df['Inauguración'].str[0]
    # df['Mánager'] = df['Mánager'].str[0]
    # df['Liga'] = df['Liga'].str[0]

    # Updating the new columns
    if 'Ubicación' not in df.columns:
        df['Ubicación'] = no_data
        df['city'] = df['Ubicación'].str.split(",")
    else:
        df['Ubicación'] = df['Ubicación'].str[0]
        df['city'] = df['Ubicación'].str.split(",")

    df['name_reported']=team_left

    # Identifying the final city column
    df['city'] = df['city'].str[0]

    return df
