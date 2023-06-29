from pipeline.connections.sftp import sftp_connection
from tempfile import NamedTemporaryFile

import os 


class SFTPClient:

    def __init__(self, connection: sftp_connection):
        self.sftp_connection = connection


    def list_files(self, path: str) -> list:
        """List files in SFTP."""

        files = list()
        
        file_list = self.sftp_connection.listdir(path)

        for file in file_list:
            item = os.path.join(path, file)
            files.append({'file': file, 'modified': self.sftp_connection.stat(item).st_mtime})

        return files
    
    def get_new_files(self, list_of_files: list, last_modified: int) -> list:
        """Get new files in SFTP."""

        new_files = []

        [new_files.append(file) for file in list_of_files if file['modified'] > last_modified]
                
        return new_files
    

    def upload_data_from_sftp_to_s3(self, s3_client, file: str, bucket_name: str, file_name: str) -> None:
        """Uploads a file from SFTP to S3."""

        with NamedTemporaryFile() as temporary_file:
            self.sftp_connection.get(file, temporary_file.name)
            
            s3_client.upload_file(temporary_file.name, bucket_name, file_name)
