from minio import Minio

from main import settings


client = Minio(
    endpoint='{}:{}'.format(
        settings.MINIO_HOST,
        settings.MINIO_PORT
    ),
    access_key=settings.MINIO_USER,
    secret_key=settings.MINIO_PASSWORD,
    secure=False,
    cert_check=False
)

