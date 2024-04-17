import pandas as pd 
from pandas import DataFrame
from datetime import datetime
from typing import List
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(data: DataFrame, *args, **kwargs):

    for index,row in data.iterrows():
        reported_date = row['transf_date'].replace(',','')
        data['clean_data'] = datetime.strptime(reported_date, '%b %d %Y').date()
    
    market_value_clean = list()
    for index, row in data.iterrows():
        reported_value = row['market_value'].strip()
        valor = reported_value[1:-1]
        if reported_value[-1] == 'm':
            market_value_clean.append(float(valor)*(1000000))
        else:
            market_value_clean.append(float(valor)*(100000))

    data_cleaned = pd.concat([data, pd.DataFrame(market_value_clean)], axis=1)
    data_cleaned.rename(columns={data_cleaned.columns[-1]: "market_value_clean"}, inplace = True)
    
    return data_cleaned
