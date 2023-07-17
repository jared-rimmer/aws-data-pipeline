def test_bucket_versioning_is_enabled(s3_client, bucket_name, create_s3_bucket):
    result = s3_client.get_bucket_versioning(Bucket=bucket_name)

    assert result["Status"] == "Enabled"


def test_bucket_versioning_is_disabled(
    s3_client, production_bucket_name, create_production_s3_bucket
):
    result = s3_client.get_bucket_versioning(Bucket=production_bucket_name)

    assert result["Status"] == "Disabled"
