from pipeline.config.connections import get_aws_connection_credentials
from pipeline.utils.s3 import s3_connection
from pipeline.clients.s3 import S3Client
from unittest.mock import patch, MagicMock

import os

def test_s3_list_files(s3_client, create_s3_bucket, bucket_name):

    first_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'fixtures', '2023-06-23-trades.csv'))
    second_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'fixtures', '2023-06-24-trades.csv'))

    s3_client.upload_file(first_file, bucket_name, '2023-06-23-trades.csv')
    s3_client.upload_file(second_file, bucket_name, '2023-06-24-trades.csv')

    result = S3Client(s3_client).list_files(bucket_name='raw-data', prefix='2023-06')

    assert result == ['2023-06-23-trades.csv', '2023-06-24-trades.csv']

def test_get_latest_file_version(s3_client, create_s3_bucket, bucket_name):

    first_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'fixtures', '2023-06-23-trades.csv'))

    s3_client.upload_file(first_file, bucket_name, '2023-06-23-trades.csv')

    test_list = ['2023-06-23-trades.csv']

    with patch.object(s3_client, 'list_object_versions', new_callable=MagicMock()) as list_object_versions: 
        list_object_versions.return_value = {'Versions': [
            {'Key': '2023-06-23-trades.csv', 'IsLatest': True, 'VersionId': '1234'},
            {'Key': '2023-06-23-trades.csv', 'IsLatest': False, 'VersionId': '5678'}
            ]}

        result = S3Client(s3_client).get_latest_file_version(bucket_name='raw-data', list_of_files=test_list)

        assert result == [{'file_name': '2023-06-23-trades.csv', 'version': '1234'}]

def test_get_file(s3_client, create_s3_bucket, bucket_name):

    first_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'fixtures', '2023-06-29-trades.csv'))
    second_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'fixtures', '2023-06-29-trades-2.csv'))

    s3_client.upload_file(first_file, bucket_name, '2023-06-29-trades.csv')
    s3_client.upload_file(second_file, bucket_name, '2023-06-29-trades.csv')

    file_versions = s3_client.list_object_versions(Bucket=bucket_name, Prefix='2023-06-29-trades.csv')
            
    latest_file = [{'file_name' : element['Key'], 'version' : element['VersionId']} for element in file_versions['Versions'] if element["IsLatest"]]
                    
    result = S3Client(s3_client).get_file(bucket_name=bucket_name, file_name=latest_file[0]['file_name'], version_id=latest_file[0]['version'])

    assert result == 'id,ticker,price,quantity,status\n1,SNOW,200,20,settled'

