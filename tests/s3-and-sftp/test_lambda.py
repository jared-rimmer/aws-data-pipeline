from dataclasses import asdict

import pytest

from pipeline.config.connections import (
    get_aws_connection_credentials,
    get_postgres_connection_credentials,
)

from pipeline.connections.postgres import database_connection

import boto3

import json

import zipfile, shutil, os


@pytest.fixture
def my_s3_client():
    s3_client = boto3.client("s3", **asdict(get_aws_connection_credentials()))
    bucket_name = "staging-data"
    s3_client.create_bucket(Bucket=bucket_name)
    yield s3_client


@pytest.fixture
def my_iam_client():
    iam = boto3.client("iam", **asdict(get_aws_connection_credentials()))
    yield iam


@pytest.fixture
def my_lambda_client():
    iam = boto3.client("lambda", **asdict(get_aws_connection_credentials()))
    yield iam


@pytest.fixture
def create_lambda_zip_file():
    virtual_env_path = os.getenv("VIRTUAL_ENV_PATH")

    shutil.make_archive("./lambda/lambda_deployment_package", "zip", virtual_env_path)

    lambda_zip_file = zipfile.ZipFile("./lambda/lambda_deployment_package.zip", "a")

    lambda_zip_file.write("./lambda/lambda_function.py", "lambda_function.py")


@pytest.fixture
def mocked_lambda_client(
    my_s3_client, my_iam_client, my_lambda_client, create_lambda_zip_file
):
    bucket_name = "staging-data"

    my_s3_client.create_bucket(Bucket=bucket_name)

    my_s3_client.upload_file(
        "./lambda/lambda_deployment_package.zip",
        bucket_name,
        "lambda_deployment_package.zip",
    )

    if "lambda-s3-role" in [
        e["RoleName"] for e in my_iam_client.list_roles().get("Roles", [])
    ]:
        my_iam_client.delete_role(RoleName="lambda-s3-role")
    iam_role = my_iam_client.create_role(
        RoleName="lambda-s3-role",
        AssumeRolePolicyDocument="""{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:ListObject"
                    ],
                    "Resource": "arn:aws:s3:::staging-data/*"
                }
            ]
        }""",
    )

    my_lambda_client.create_function(
        FunctionName="custom-lambda-function",
        Runtime="python3.8",
        Role=iam_role["Role"]["Arn"],
        Handler="lambda_function.lambda_handler",
        Code={
            "S3Bucket": "staging-data",
            "S3Key": "lambda_deployment_package.zip",
        },
        Environment={
            "Variables": {
                "DATABASE_HOST": os.getenv("DATABASE_HOST"),
                "DATABASE_NAME": os.getenv("DATABASE_NAME"),
                "DATABASE_USERNAME": os.getenv("DATABASE_USERNAME"),
                "DATABASE_PASSWORD": os.getenv("DATABASE_PASSWORD"),
                "PYTHONPATH": "/moto/src",
            }
        },
    )

    yield my_lambda_client


@pytest.fixture
def set_up_tear_down():
    with database_connection(get_postgres_connection_credentials()) as db_cur:
        db_cur.run("truncate table production.trades")

    yield

    with database_connection(get_postgres_connection_credentials()) as db_cur:
        db_cur.run("truncate table production.trades")


def test_invoking_lambda(mocked_lambda_client, set_up_tear_down):
    response = mocked_lambda_client.invoke(FunctionName="custom-lambda-function")

    parsed = json.loads(response["Payload"].read().decode("utf-8"))

    with database_connection(get_postgres_connection_credentials()) as db_cur:
        result = db_cur.run("select count(*) from production.trades")[0][0]

    assert parsed == None
    assert result == 3
