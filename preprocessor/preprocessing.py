import pandas as pd
import numpy as np

from datetime import datetime
import os

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

load_dotenv()

DATAPATH = 'data'

#preprocessing steps:
#function to remove currency sign from price
def remove_currency(x):
    try:
        return x.split(' ')[1]
    except Exception as e:
        return x

#function to remove character from vegetable names which will be used as column
def clean_columns(column):
    _list = []
    for x in column:
        try:
            a = x.lower().replace('(', ' ').replace(")", '').split(' ')
            a = '_'.join(a)
            _list.append(a)
        except Exception as e:
            _list.append('unknown')

    return _list


#function to get the date 
def get_date(path):
    return datetime.strptime(path.split('/')[-1].split('.')[0],"%m-%d-%Y")

#function to check if a dataset contains data or not
def valid_dataset(dataset):
    if dataset['commodities'].iloc[0] == "No data available in table":
        return False
    else:
        return True
        
#function to transform entire dataset into a row for new column
def transform(dataset, date):
    if valid_dataset(dataset):
        
        dataset['average'] = dataset['average'].astype(str).apply(lambda a: remove_currency(a))    
        dataset = dataset[['commodities',  'average']]
        
        dataset = dataset.T
        # print(dataset.iloc[0])
        dataset.columns = clean_columns(list(dataset.iloc[0]))
        dataset = dataset[1:]
        dataset.reset_index(drop = True)
 
        date = get_date(date)
        dataset['date'] = date
        dataset['no_data_available'] = False
        dataset.set_index('date', inplace = True, drop = True)
        return dataset
    else:
        date = get_date(date)
        throwaway_dataset = {'no_data_available': True, 'date': date}
        dataset = pd.DataFrame(throwaway_dataset, index = [1]).set_index('date')
        return dataset
    



# Connecting to Container Client 
load_dotenv()

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container=container_name)

blobs = container_client.list_blob_names()
if not os.path.exists('data'): os.makedirs('data')

# Download the unprocessed csv files from azure container 
for blob in blobs:
    print(f"downloading {blob}")

    blob_client = container_client.get_blob_client(blob)
    with open(blob, 'wb') as f:
        f.write(blob_client.download_blob().readall())


# Applying transformations to all the raw data files and the mergin the transformed data into the scrapped dataset    
scrapped_dataset = None
for i,data in enumerate(os.listdir(DATAPATH)):
    file_path = os.path.join(DATAPATH, data)
    if i == 0:
        dataset = pd.read_csv(file_path)
        dataset = transform(dataset, file_path)
        scrapped_dataset = dataset
    else:
        dataset = pd.read_csv(file_path)
        dataset = transform(dataset, file_path)
        scrapped_dataset = pd.concat([scrapped_dataset, dataset], ignore_index = False, sort = False)


# Download the latest version of the data from azure blob storage
if not os.path.exists('latest.csv'):
    raise FileNotFoundError("Could not load the latest version of the data")
else:
    current_data = pd.read_csv('latest.csv')
    print(f"shape of the current data = {current_data.shape}")


# merge the current batch of data with the previous version of the data resulting in new version
try:
    latest_version = pd.concat([current_data, scrapped_dataset], ignore_index=False, sort = False)
    latest_version.shape
except Exception as e:
    print("could not merge the previous version of the data with this batch", e)
    exit(1)

latest_version.to_csv('latest.csv')

blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_path)
with open(file_path, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded: {file_path}")

# Removing the data from the azure storage blob

blobs = container_client.list_blob_names()
for blob in blobs:
    if blob.startswith('data/'):
        blob_client = container_client.get_blob_client(blob)

        print(f"attempting to delete blob: {blob}")

        try:
            blob_client.delete_blob()
            print(f"deleted {blob}")
        except Exception as e:
            print(f"failed to delete blob: {blob}")

