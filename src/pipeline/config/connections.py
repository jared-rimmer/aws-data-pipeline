from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class SFTPConnectionConfig:
    username: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: int = 22


def get_sftp_connection_credentials() -> SFTPConnectionConfig:
    return SFTPConnectionConfig(
        username=os.environ.get('SFTP_USERNAME', ''),
        password=os.environ.get('SFTP_PASSWORD', ''),
        host=os.environ.get('SFTP_HOST', ''),
        port=int(os.environ.get('SFTP_PORT', 22))
    )