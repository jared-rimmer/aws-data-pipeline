from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class SFTPConnectionConfig:
    username: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: int = 22


def get_sftp_connection_credentials() -> SFTPConnectionConfig:
    return SFTPConnectionConfig(
        username=os.environ.get('SFTP_USERNAME', ''),
        password=os.environ.get('SFTP_PASSWORD', ''),
        host=os.environ.get('SFTP_HOST', ''),
        port=int(os.environ.get('SFTP_PORT', 22))
    )

@dataclass
class PostgresConnectionConfig:
    user: Optional[str]
    password: Optional[str]
    host: Optional[str]
    database: Optional[str]
    port: int = 5432

def get_postgres_connection_credentials() -> PostgresConnectionConfig:
    return PostgresConnectionConfig(
        user=os.environ.get('DATABASE_USERNAME', ''),
        password=os.environ.get('DATABASE_PASSWORD', ''),
        host=os.environ.get('DATABASE_HOST', ''),
        database=os.environ.get('DATABASE_NAME', ''),
        port=os.environ.get('DATABASE_PORT', 5432)
    )

@dataclass
class AWSConnectionConfig:
    aws_access_key_id: Optional[str]
    aws_secret_access_key: Optional[str]
    region_name: Optional[str]
    endpoint_url: Optional[str]


def get_aws_connection_credentials() -> AWSConnectionConfig:
    return AWSConnectionConfig(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''),
        region_name=os.environ.get('AWS_REGION_NAME', ''),
        endpoint_url=os.environ.get('AWS_ENDPOINT_URL', '')
    )