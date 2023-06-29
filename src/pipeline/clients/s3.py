from pipeline.connections.s3 import s3_connection


class S3Client:

    def __init__(self, connection: s3_connection):
        self.client = connection


    def list_files(self, bucket_name: str, prefix: str) -> list:

        s3_objects = self.client.list_objects(Bucket=bucket_name, Prefix=prefix) 
        contents = s3_objects.get('Contents', False)
        if contents:
            return list(map(lambda x: x['Key'], contents))
        else:
            return []
        
    def get_latest_file_version(self, bucket_name: str, list_of_files: list):

        latest_files = []

        for file in list_of_files:
            versions = self.client.list_object_versions(Bucket=bucket_name, Prefix=file)
            for element in versions['Versions']:
                if element["IsLatest"]:
                    latest_files.append({'file_name' : element['Key'], 'version' : element['VersionId']})
        
        return latest_files
    

    def get_file(self, bucket_name: str, file_name: str, version_id: str):

        file = self.client.get_object(Bucket=bucket_name, Key=file_name, VersionId=version_id)
        
        return file['Body'].read().decode('utf-8')
        

