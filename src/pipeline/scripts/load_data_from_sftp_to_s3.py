from tempfile import NamedTemporaryFile

from pipeline.config.connections import get_sftp_connection_credentials
from pipeline.utils.sftp import sftp_connection

def upload_data_from_sftp_to_s3(s3_client, file: str, bucket_name: str, file_name: str) -> None:
    """Uploads a file from SFTP to S3."""

    with NamedTemporaryFile() as temporary_file:
        with sftp_connection(get_sftp_connection_credentials()) as sftp_conn:
            sftp_conn.get(file, temporary_file.name)
        
        s3_client.upload_file(temporary_file.name, bucket_name, file_name)
