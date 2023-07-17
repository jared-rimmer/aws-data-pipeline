import boto3
import pytest

from moto import mock_s3


@pytest.fixture
def s3_client():
    """Mocked S3 Client using moto contextmanager"""

    with mock_s3():
        conn = boto3.client("s3", region_name="us-east-1")
        yield conn


@pytest.fixture
def bucket_name():
    return "raw-data"


@pytest.fixture
def create_s3_bucket(s3_client, bucket_name):
    s3_client.create_bucket(Bucket=bucket_name)

    s3_client.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={"MFADelete": "Disabled", "Status": "Enabled"},
    )

    yield


@pytest.fixture
def production_bucket_name():
    return "prod-data"


@pytest.fixture
def create_production_s3_bucket(s3_client, production_bucket_name):
    s3_client.create_bucket(Bucket=production_bucket_name)

    s3_client.put_bucket_versioning(
        Bucket=production_bucket_name,
        VersioningConfiguration={"MFADelete": "Disabled", "Status": "Disabled"},
    )

    yield


def delete_files_and_versions(s3_client, bucket_name, prefix):
    paginator = s3_client.get_paginator("list_object_versions")
    response_iterator = paginator.paginate(Bucket=bucket_name)
    for response in response_iterator:
        versions = response.get("Versions", [])
        versions.extend(response.get("DeleteMarkers", []))
        for result in [
            {"filename": x["Key"], "version_id": x["VersionId"]}
            for x in versions
            if prefix in x["Key"] and x["VersionId"] != "null"
        ]:
            s3_client.delete_object(
                Bucket=bucket_name,
                Key=result["filename"],
                VersionId=result["version_id"],
            )


@pytest.fixture
def set_up_and_tear_down(s3_client, bucket_name):
    """Removes all files and versions from the staging bucket"""

    prefix = "2023-06"

    delete_files_and_versions(s3_client, bucket_name, prefix)

    yield

    delete_files_and_versions(s3_client, bucket_name, prefix)
