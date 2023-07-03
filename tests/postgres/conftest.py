import os
import pytest


@pytest.fixture
def postgres_credentials():
    """Mocked SFTP Credentials"""
    os.environ['DATABASE_USERNAME'] = 'postgres'
    os.environ['DATABASE_PASSWORD'] = 'postgres'
    os.environ['DATABASE_HOST'] = '127.0.0.1'
    os.environ['DATABASE_NAME'] = 'postgres'
    os.environ['DATABASE_PORT'] = '5432'
