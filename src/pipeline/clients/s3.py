from pipeline.connections.s3 import s3_connection


class S3Client:
    def __init__(self, connection: s3_connection):
        self.client = connection

    def list_files(self, bucket_name: str, prefix: str = "") -> set:
        if prefix:
            s3_objects = self.client.list_objects(Bucket=bucket_name, Prefix=prefix)

        else:
            s3_objects = self.client.list_objects(Bucket=bucket_name)

        contents = s3_objects.get("Contents", False)
        if contents:
            return set(map(lambda x: x["Key"], contents))
        else:
            return {}

    def get_latest_file_version(self, bucket_name: str, list_of_files: list):
        latest_files = []

        for file in list_of_files:
            versions = self.client.list_object_versions(Bucket=bucket_name, Prefix=file)
            for element in versions["Versions"]:
                if element["IsLatest"]:
                    latest_files.append(
                        {"file_name": element["Key"], "version": element["VersionId"]}
                    )

        return latest_files

    def get_file(self, bucket_name: str, file_name: str, version_id: str = ""):
        if version_id:
            file = self.client.get_object(
                Bucket=bucket_name, Key=file_name, VersionId=version_id
            )
        else:
            file = self.client.get_object(Bucket=bucket_name, Key=file_name)

        return file["Body"].read().decode("utf-8")

    def put_file(self, bucket_name: str, file_name: str, file_content: str) -> None:
        self.client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)

    def delete_file_by_suffix(
        self, bucket_name: str, suffix: str, latest_file_name: str
    ) -> None:
        files = self.client.list_objects(Bucket=bucket_name)

        for file in files["Contents"]:
            if file["Key"] != latest_file_name and suffix in file["Key"]:
                self.client.delete_object(Bucket=bucket_name, Key=file["Key"])
