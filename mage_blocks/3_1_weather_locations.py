from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
from datetime import datetime, timedelta
import pandas as pd
from pandas import DataFrame

@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    """
    Template for loading data from a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    # To get the data in a new file, we prepare the file name
    today = datetime.now().date()
    # yesterday = today - timedelta(days = 1)
    day_name = today.strftime("%A")
    number_day = today.strftime("%d")
    month_name = today.strftime("%b")
    month_number = today.strftime("%m")
    year = today.strftime("%Y")
    dataset_file = f'cities_info_{year}_{month_name}_{number_day}_{day_name}'
    
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'soccer-dataset_data-taxi-1' # Bucket Destination
    object_key = f'data/city_data/{year}/{month_number}_{month_name}/{dataset_file}.csv'  # The path to store in GCS

    print('Loading the file: ',{dataset_file},'.csv into gcs')

    data_raw = GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )

    return data_raw