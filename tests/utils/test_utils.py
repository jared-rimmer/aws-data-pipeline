from pipeline.utils.utils import set_source_file_name, add_source_file_name, set_new_source_files


def test_generate_new_file_name():

    result = set_source_file_name(latest_file={'version': 'abc-123-xyz-987', 'file_name': 'trades.csv'})

    assert result == 'abc-123-xyz-987-trades.csv'


def test_generate_new_file_name_with_int_version():

    result = set_source_file_name(latest_file={'version': 1234, 'file_name': 'trades.csv'})

    assert result == '1234-trades.csv'


def test_set_latest_source_files_in_s3():

    test_latest_files = [
        {'version': 'abc-123-xyz-987', 'file_name': 'trades.csv'},
        {'version': 'xyz-987-abc-123', 'file_name': 'trades.csv'}]

    result = add_source_file_name(latest_files=test_latest_files)

    assert result == [
        {'version': 'abc-123-xyz-987', 'file_name': 'trades.csv', 'source_file_name': 'abc-123-xyz-987-trades.csv'},
        {'version': 'xyz-987-abc-123', 'file_name': 'trades.csv', 'source_file_name': 'xyz-987-abc-123-trades.csv'}
    ]


def test_set_new_source_files():

    test_s3_sources = [
        {'version': 'abc-123-xyz-987', 'file_name': 'trades.csv', 'source_file_name': 'abc-123-xyz-987-trades.csv'},
        {'version': 'xyz-987-abc-123', 'file_name': 'trades.csv', 'source_file_name': 'xyz-987-abc-123-trades.csv'}
    ]

    test_database_sources = {'abc-123-xyz-987-trades.csv'}

    result = set_new_source_files(s3_files=test_s3_sources, database_sources=test_database_sources)

    assert result == {'xyz-987-abc-123-trades.csv'}