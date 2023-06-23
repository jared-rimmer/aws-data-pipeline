from pipeline.scripts.load_data_from_sftp_to_s3 import upload_data_from_sftp_to_s3


def test_upload_data_from_sftp_to_s3(s3_client, create_s3_bucket, sftp_credentials, bucket_name):
    
    upload_data_from_sftp_to_s3(s3_client, file='upload/2023-06-23-trades.csv', bucket_name=bucket_name, file_name='2023-06-23-trades.csv')

    result = s3_client.list_objects(Bucket=bucket_name, Prefix='2023-06-23-trades')
    
    assert result['Contents'][0]['Key'] == '2023-06-23-trades.csv'

