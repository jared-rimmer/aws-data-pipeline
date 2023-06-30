def set_source_file_name(latest_file: dict) -> str:

    return str(latest_file['version']) + '-' + latest_file['file_name']


def add_source_file_name(latest_files: list) -> set:

    for file in latest_files:
        file['source_file_name'] = set_source_file_name(latest_file=file)

    return latest_files


def set_new_source_files(s3_files: list, database_sources: set) -> set:

    s3_sources = set([file['source_file_name'] for file in s3_files])

    return set(s3_sources).difference(database_sources)

