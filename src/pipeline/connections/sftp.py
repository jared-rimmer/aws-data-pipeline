from contextlib import contextmanager
from dataclasses import asdict

import pysftp

from pipeline.config.connections import SFTPConnectionConfig


@contextmanager
def sftp_connection(sftp_connection_config: SFTPConnectionConfig):
    connection_options = pysftp.CnOpts()
    connection_options.hostkeys = None
    sftp_conn = pysftp.Connection(
        **asdict(sftp_connection_config), private_key=".ppk", cnopts=connection_options
    )

    try:
        yield sftp_conn
    finally:
        sftp_conn.close()
