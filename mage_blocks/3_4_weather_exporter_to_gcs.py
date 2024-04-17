from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path
from datetime import datetime, timedelta

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:

    # To get the data in a new file, we prepare the file name
    today = datetime.now().date()
    # yesterday = today - timedelta(days = 1)
    day_name = today.strftime("%A")
    number_day = today.strftime("%d")
    month_name = today.strftime("%b")
    month_number = today.strftime("%m")
    year = today.strftime("%Y")
    dataset_file = f'weather_{year}_{month_name}_{number_day}_{day_name}'
    
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'soccer-dataset_data-taxi-1' # Bucket Destination
    object_key = f'data/weather_data/{year}/{month_number}_{month_name}/{dataset_file}.csv'  # The path to store in GCS

    print('Uploading the file: ',{dataset_file},'.csv into gcs')

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )

    print('The file: ',{dataset_file},'.csv was succesfully uploaded')
