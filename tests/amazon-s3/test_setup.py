def test_bucket_versioning_is_enabled(s3_client, bucket_name, create_s3_bucket):

    result = s3_client.get_bucket_versioning(Bucket=bucket_name)

    assert result['Status'] == 'Enabled'
