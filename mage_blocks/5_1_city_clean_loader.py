from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from datetime import datetime, timedelta
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_from_google_cloud_storage(*args, **kwargs):

    # To get the data in a new file, we prepare the file name
    today = datetime.now().date()
    yesterday = today - timedelta(days = 1)
    day_name = yesterday.strftime("%A")
    number_day = yesterday.strftime("%d")
    month_name = yesterday.strftime("%b")
    month_number = yesterday.strftime("%m")
    year = yesterday.strftime("%Y")
    dataset_file = f'{year}_{month_name}_{number_day}_{day_name}'
    
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'soccer-dataset_data-taxi-1' # Bucket Origin
    object_key = f'data/city_data/{year}/{month_number}_{month_name}/{dataset_file}.csv'  # The path to store in GCS

    print('Loading the file: ',{dataset_file},'.csv into gcs')

    data = GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )

    return data