from pipeline.config.connections import get_sftp_connection_credentials
from pipeline.connections.sftp import sftp_connection
from pipeline.clients.sftp import SFTPClient


def test_upload_data_from_sftp_to_s3(s3_client, create_s3_bucket, bucket_name):

    files_to_upload = [
        {'file': '2023-06-23-trades.csv', 'modified': 1687516497},
        {'file': '2023-06-24-trades.csv', 'modified': 1687783811},
        {'file': '2023-06-25-trades.csv', 'modified': 1687783815},
    ]

    with sftp_connection(get_sftp_connection_credentials()) as sftp_conn:

        for file in files_to_upload:
        
            SFTPClient(sftp_conn).upload_data_from_sftp_to_s3(s3_client, file=f'upload/{file["file"]}', bucket_name=bucket_name, file_name=file['file'])

    result = s3_client.list_objects(Bucket=bucket_name, Prefix='2023-06')
            
    assert result['Contents'][0]['Key'] == '2023-06-23-trades.csv'
    assert result['Contents'][1]['Key'] == '2023-06-24-trades.csv'
    assert result['Contents'][2]['Key'] == '2023-06-25-trades.csv'


def test_versioning_with_upload_data_from_sftp_to_s3(s3_client, create_s3_bucket, bucket_name, set_up_and_tear_down):

    with sftp_connection(get_sftp_connection_credentials()) as sftp_conn:

        SFTPClient(sftp_conn).upload_data_from_sftp_to_s3(s3_client, file='upload/2023-06-23-trades.csv', bucket_name=bucket_name, file_name='2023-06-23-trades.csv')
        SFTPClient(sftp_conn).upload_data_from_sftp_to_s3(s3_client, file='upload/2023-06-23-trades.csv', bucket_name=bucket_name, file_name='2023-06-23-trades.csv')

    result = s3_client.list_object_versions(Bucket=bucket_name, Prefix='2023-06-23-trades')
    
    assert len(result["Versions"]) == 2
    assert result["Versions"][0]['IsLatest'] == True
    assert result["Versions"][1]['IsLatest'] == False
