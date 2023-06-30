from pipeline.utils.utils import set_source_file_name, add_source_file_name, get_difference


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


def test_get_difference_s3_set_one():

    test_s3_sources = {'abc-123-xyz-987-trades.csv', 'xyz-987-abc-123-trades.csv'}

    test_database_sources = {'abc-123-xyz-987-trades.csv', 'bla-bla.csv'}

    result = get_difference(set_one=test_s3_sources, set_two=test_database_sources)

    assert result == {'xyz-987-abc-123-trades.csv'}


def test_get_difference_database_set_one():

    test_s3_sources = {'abc-123-xyz-987-trades.csv', 'xyz-987-abc-123-trades.csv'}

    test_database_sources = {'abc-123-xyz-987-trades.csv', 'bla-bla.csv'}

    result = get_difference(set_one=test_database_sources, set_two=test_s3_sources)

    assert result == {'bla-bla.csv'}