from tempfile import NamedTemporaryFile

from pipeline.config.connections import get_sftp_connection_credentials
from pipeline.utils.sftp import sftp_connection

import os 

def upload_data_from_sftp_to_s3(s3_client, file: str, bucket_name: str, file_name: str) -> None:
    """Uploads a file from SFTP to S3."""

    with NamedTemporaryFile() as temporary_file:
        with sftp_connection(get_sftp_connection_credentials()) as sftp_conn:
            sftp_conn.get(file, temporary_file.name)
        
        s3_client.upload_file(temporary_file.name, bucket_name, file_name)

def list_files_in_sftp(sftp_client, path: str) -> list:
    """List files in SFTP."""

    files = []
    
    file_list = sftp_client.listdir(path)

    for file in file_list:
        item = os.path.join(path, file)

        files.append({'file': file, 'modified': sftp_client.stat(item).st_mtime})

    return files


def get_new_files(list_of_files: list, last_modified: int) -> list:
    """Get new files in SFTP."""

    new_files = []

    for file in list_of_files:
        if file['modified'] > last_modified:
            new_files.append(file)

    return new_files

from tempfile import NamedTemporaryFile


def upload_data_from_sftp_to_s3(s3_client, file: str, bucket_name: str, file_name: str) -> None:
    """Uploads a file from SFTP to S3."""

    with NamedTemporaryFile() as temporary_file:
        with sftp_connection(get_sftp_connection_credentials()) as sftp_conn:
            sftp_conn.get(file, temporary_file.name)
        
        s3_client.upload_file(temporary_file.name, bucket_name, file_name)
