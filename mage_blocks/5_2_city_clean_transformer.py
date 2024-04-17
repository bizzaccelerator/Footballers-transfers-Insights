import pandas as pd
from pandas import DataFrame
from datetime import datetime, timedelta

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def execute_transformer_action(data: DataFrame, *args, **kwargs) -> DataFrame:

    columns = {
                'Nombre': 'nombre',
                'Apodo(s)': 'apodo',
                'Fundación': 'fundacion',
                'Presidente': 'presidente',
                'Entrenador': 'entrenador',
                'Estadio': 'estadio',
                'Ubicación': 'ubicacion',
                'Capacidad': 'capacidad',
                'name_reported': 'team_name',
    }
    
    data.rename(columns = columns, inplace = True)
    
    # Selecting the final set of columns 
    data = data[['nombre','apodo', 'fundacion', 'presidente', 'entrenador', 'estadio', 'ubicacion', 'capacidad', 'city', 'team_name',]]

    # To organize the columns 
    data['capacidad'] = data['capacidad'].astype(str)

    # To get the date in the file:
    today = datetime.now().date()
    yesterday = today - timedelta(days = 1)
    day_name = yesterday.strftime("%A")
    number_day = yesterday.strftime("%d")
    month_name = yesterday.strftime("%b")
    month_number = yesterday.strftime("%m")
    year = yesterday.strftime("%Y")
    # dataset_date = f'{year}-{month_number}-{number_day}'
    dataset_date = '2024-04-03'

    data['date'] = dataset_date
    data['date'] = data['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    return data
