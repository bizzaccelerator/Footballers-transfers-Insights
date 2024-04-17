from datetime import datetime
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(data, *args, **kwargs):
    
    # To get the date
    try: 
      data['timestamp'] = data['timestamp'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    except:
      data['timestamp'] = ""

    data['date'] = data['timestamp'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    
    # To organize the columns 
    data['latitude'] = data['latitude'].astype(str)
    data['longitude'] = data['longitude'].astype(str)

    return data

