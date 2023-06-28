from pipeline.config.connections import get_sftp_connection_credentials
from pipeline.utils.sftp import sftp_connection
from pipeline.clients.sftp import SFTPClient


from unittest.mock import patch, MagicMock

def test_file_list(sftp_credentials):
    with sftp_connection(get_sftp_connection_credentials()) as sftp_conn:
        with patch.object(sftp_conn, 'stat', new_callable=MagicMock()) as stat:       
            stat.return_value = MagicMock(st_mtime=1687516497)   

            result = SFTPClient(sftp_conn).list_files(path='upload')

            assert result == [
                {'file': '2023-06-23-trades.csv', 'modified': 1687516497},
                {'file': '2023-06-24-trades.csv', 'modified': 1687516497},
                {'file': '2023-06-25-trades.csv', 'modified': 1687516497},
            ]


def test_get_new_files():

    test_files = [
        {'file': '2023-06-23-trades.csv', 'modified': 1687516497},
        {'file': '2023-06-24-trades.csv', 'modified': 1687783811},
        {'file': '2023-06-25-trades.csv', 'modified': 1687783815},

    ]

    with sftp_connection(get_sftp_connection_credentials()) as sftp_conn:
        result = SFTPClient(sftp_conn).get_new_files(list_of_files=test_files, last_modified=1687516498)

        assert result == [
            {'file': '2023-06-24-trades.csv', 'modified': 1687783811},
            {'file': '2023-06-25-trades.csv', 'modified': 1687783815}
        ]
