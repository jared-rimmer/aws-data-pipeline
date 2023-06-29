from contextlib import contextmanager
from dataclasses import asdict

import boto3

from pipeline.config.connections import AWSConnectionConfig

@contextmanager
def s3_connection(aws_connection_config: AWSConnectionConfig):
    
    s3_connection = boto3.client("s3", **asdict(aws_connection_config))

    try:
        yield s3_connection
    finally:
        s3_connection.close()
