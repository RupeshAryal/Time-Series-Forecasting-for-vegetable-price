from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")


class AzureUpload:
    def __init__(self, connection_string, container_name):
        self.connection_string = connection_string
        self.container_name = container_name

        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        except Exception as e:
            raise ConnectionAbortedError("unable to start connection to azure blob client." \
            "Is the connection sttring valid?")

        try:
            self.blob_service_client.create_container(container_name)
        except Exception as e:
            logging.warning(f"container: {container_name} already exists. Using the exisiting container for further operations")

    def upload_file(self, file_path):
        if os.path.isfile(file_path):
            if os.path.getsize(file_path) < (200 * 1024):
                logging.info(f"uploading {file_path} to azure cloud storage")

                blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=file_path)
                with open(file_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)
                    print(f"Uploaded: {file_path}")

                logging.info(f"successfully uploaded {file_path} to container: {self.container_name}")
            
            else:
                logging.warning(f"The blob is larger than 200kb. Skipped uploading")
        else:
            raise IsADirectoryError(f"Expected a file. {file_path} is a directory. ")
        








        





        


