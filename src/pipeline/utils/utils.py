def set_source_file_name(latest_file: dict) -> str:
    return str(latest_file["version"]) + "-" + latest_file["file_name"]


def add_source_file_name(latest_files: list) -> set:
    for file in latest_files:
        file["source_file_name"] = set_source_file_name(latest_file=file)

    return latest_files


def get_difference(set_one: set, set_two: set) -> set:
    return set(set_one).difference(set_two)
