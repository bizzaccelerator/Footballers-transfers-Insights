from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path
from datetime import datetime, timedelta
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
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

    bucket_name = 'soccer-dataset_data-taxi-1' # Bucket Destination
    object_key = f'data/players_data/{year}/{month_number}_{month_name}/{dataset_file}.csv'  # The path to store in GCS

    print('Uploading the file: ',{dataset_file},'.csv into gcs')

    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    GoogleCloudStorage.with_config(ConfigFileLoader(credentials_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )
    
    print('The file: ',{dataset_file},'.csv was succesfully uploaded')