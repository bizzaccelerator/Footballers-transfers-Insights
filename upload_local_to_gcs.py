from google.cloud import storage
import os

# Upload the CSV file to GCS
file_name = "2024_Apr_08_Monday.csv"
csv_filename = f"C://Users/jober/OneDrive/Desktop/Footballers_transfers_Insights/data/players_data/2024/04_Apr/{file_name}"
# csv_filename = f"C://Users/jober/OneDrive/Desktop/Footballers_transfers_Insights/data/city_data/2024/04_Apr/{file_name}"
# csv_filename = f"C://Users/jober/OneDrive/Desktop/Footballers_transfers_Insights/data/weather_data/2024/04_Apr/{file_name}"

bucket_name = 'soccer-dataset_data-taxi-1' # Destination
destination_blob_name = f'data/players_data/2024/04_Apr/{file_name}'  # The path to store in GCS

# set key credentials file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C://Users/jober/OneDrive/Desktop/Footballers_transfers_Insights/credentials/data-taxi-1-a1d4e91c10cd.json'

# define function that uploads a file from the bucket
def upload_cs_file(bucket_name, csv_filename, destination_blob_name): 
    storage_client = storage.Client()  # Instanciate a client
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(csv_filename)
    return True

upload_cs_file(bucket_name, csv_filename, destination_blob_name)

print(f"File {file_name} uploaded to GCS bucket {bucket_name} as {destination_blob_name}")