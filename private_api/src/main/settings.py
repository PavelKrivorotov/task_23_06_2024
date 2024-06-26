import os
from pathlib import Path

import dotenv


BaseDir = Path(__file__).parent
dotenv.load_dotenv(Path(BaseDir.parent.parent.parent, '.env'))


HOST = os.getenv('PRIVATE_API_HOST')
PORT = int(os.getenv('PRIVATE_API_PORT'))

MINIO_HOST = os.getenv('MINIO_HOST')
MINIO_PORT = int(os.getenv('MINIO_PORT'))
MINIO_USER = os.getenv('MINIO_USER')
MINIO_PASSWORD = os.getenv('MINIO_PASSWORD')

MINIO_EXTERNAL_HOST=os.getenv('MINIO_EXTERNAL_HOST')
MINIO_EXTERNAL_PORT=int(os.getenv('MINIO_EXTERNAL_PORT'))

