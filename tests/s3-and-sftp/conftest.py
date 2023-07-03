import boto3
import os
import pytest

from moto import mock_s3

@pytest.fixture
def sftp_credentials():
    """Mocked SFTP Credentials"""
    os.environ["SFTP_USERNAME"] = "extract"
    os.environ["SFTP_PASSWORD"] = "password"
    os.environ["SFTP_HOST"] = "localhost"
    os.environ["SFTP_PORT"]= "2222"


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_REGION_NAME"] = "us-east-1"
    os.environ["AWS_ENDPOINT_URL"] = "http://localhost:5000"

@pytest.fixture
def s3_client(aws_credentials):
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
        VersioningConfiguration={
            'MFADelete': 'Disabled',
            'Status': 'Enabled'
        }
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
        VersioningConfiguration={
            'MFADelete': 'Disabled',
            'Status': 'Disabled'
        }
    )

    yield