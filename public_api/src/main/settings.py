import os
from pathlib import Path

import dotenv


BaseDir = Path(__file__).parent
dotenv.load_dotenv(Path(BaseDir.parent.parent.parent, '.env'))


HTTP_PROTOCOL = 'http'
HOST = os.getenv('PUBLIC_API_HOST')
PORT = int(os.getenv('PUBLIC_API_PORT'))

EXTERNAL_HOST = os.getenv('PUBLIC_API_EXTERNAL_HOST')
EXTERNAL_PORT = int(os.getenv('PUBLIC_API_EXTERNAL_PORT'))

DATABASE = {
    'DRIVERNAME': 'postgresql',
    'USER': os.getenv('POSTGRES_USER'),
    'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    'NAME': os.getenv('POSTGRES_DB'),
    'HOST': os.getenv('POSTGRES_HOST'),
    'PORT': int(os.getenv('POSTGRES_PORT'))
}

BUCKET_OBJECT_SALT = 8

