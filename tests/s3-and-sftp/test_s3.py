from pipeline.clients.s3 import S3Client
from unittest.mock import patch, MagicMock

import os


def test_s3_list_files_with_prefix(
    s3_client, create_s3_bucket, bucket_name, set_up_and_tear_down
):
    first_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "fixtures", "2023-06-23-trades.csv"
        )
    )
    second_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "fixtures", "2023-06-24-trades.csv"
        )
    )

    s3_client.upload_file(first_file, bucket_name, "2023-06-23-trades.csv")
    s3_client.upload_file(second_file, bucket_name, "2023-06-24-trades.csv")

    result = S3Client(s3_client).list_files(bucket_name="raw-data", prefix="2023-06")

    assert result == {"2023-06-23-trades.csv", "2023-06-24-trades.csv"}


def test_s3_list_files_without_prefix(
    s3_client, create_s3_bucket, bucket_name, set_up_and_tear_down
):
    first_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "fixtures", "2023-06-23-trades.csv"
        )
    )
    second_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "fixtures", "2023-06-24-trades.csv"
        )
    )

    s3_client.upload_file(first_file, bucket_name, "2023-06-23-trades.csv")
    s3_client.upload_file(second_file, bucket_name, "2023-06-24-trades.csv")

    result = S3Client(s3_client).list_files(bucket_name="raw-data")

    assert result == {"2023-06-23-trades.csv", "2023-06-24-trades.csv"}


def test_get_latest_file_version(
    s3_client, create_s3_bucket, bucket_name, set_up_and_tear_down
):
    first_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "fixtures", "2023-06-23-trades.csv"
        )
    )

    s3_client.upload_file(first_file, bucket_name, "2023-06-23-trades.csv")

    test_list = ["2023-06-23-trades.csv"]

    with patch.object(
        s3_client, "list_object_versions", new_callable=MagicMock()
    ) as list_object_versions:
        list_object_versions.return_value = {
            "Versions": [
                {"Key": "2023-06-23-trades.csv", "IsLatest": True, "VersionId": "1234"},
                {
                    "Key": "2023-06-23-trades.csv",
                    "IsLatest": False,
                    "VersionId": "5678",
                },
            ]
        }

        result = S3Client(s3_client).get_latest_file_version(
            bucket_name="raw-data", list_of_files=test_list
        )

        assert result == [{"file_name": "2023-06-23-trades.csv", "version": "1234"}]


def test_get_file(s3_client, create_s3_bucket, bucket_name, set_up_and_tear_down):
    first_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "fixtures", "2023-06-29-trades.csv"
        )
    )
    second_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "fixtures", "2023-06-29-trades-2.csv"
        )
    )

    s3_client.upload_file(first_file, bucket_name, "2023-06-29-trades.csv")
    s3_client.upload_file(second_file, bucket_name, "2023-06-29-trades.csv")

    file_versions = s3_client.list_object_versions(
        Bucket=bucket_name, Prefix="2023-06-29-trades.csv"
    )

    latest_file = [
        {"file_name": element["Key"], "version": element["VersionId"]}
        for element in file_versions["Versions"]
        if element["IsLatest"]
    ]

    result = S3Client(s3_client).get_file(
        bucket_name=bucket_name,
        file_name=latest_file[0]["file_name"],
        version_id=latest_file[0]["version"],
    )

    assert result == "id,ticker,price,quantity,status\n1,SNOW,200,20,settled"


def test_put_file(
    s3_client, create_production_s3_bucket, production_bucket_name, set_up_and_tear_down
):
    file_content = "id,ticker,price,quantity,status\n1,SNOW,200,20,settled"

    S3Client(s3_client).put_file(
        bucket_name=production_bucket_name,
        file_name="2023-06-29-trades.csv",
        file_content=file_content,
    )

    result = s3_client.get_object(
        Bucket=production_bucket_name, Key="2023-06-29-trades.csv"
    )

    assert result["Body"].read().decode("utf-8") == file_content


def test_delete_file_by_prefix(
    s3_client, create_production_s3_bucket, production_bucket_name, set_up_and_tear_down
):
    first_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "fixtures", "2023-06-29-trades.csv"
        )
    )

    s3_client.upload_file(first_file, production_bucket_name, "2023-06-29-trades.csv")
    s3_client.upload_file(
        first_file, production_bucket_name, "xyz-987-abc-123-2023-06-29-trades.csv"
    )
    s3_client.upload_file(first_file, production_bucket_name, "2023-06-30-trades.csv")

    S3Client(s3_client).delete_file_by_suffix(
        bucket_name=production_bucket_name,
        suffix="2023-06-29-trades.csv",
        latest_file_name="xyz-987-abc-123-2023-06-29-trades.csv",
    )

    result = s3_client.list_objects(Bucket=production_bucket_name)

    assert result["Contents"][0]["Key"] == "2023-06-30-trades.csv"
    assert result["Contents"][1]["Key"] == "xyz-987-abc-123-2023-06-29-trades.csv"
