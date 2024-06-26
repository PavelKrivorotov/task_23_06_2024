from main import settings


def replace_host(url: str) -> str:
    old = '{0}:{1}'.format(
        settings.MINIO_HOST,
        settings.MINIO_PORT
    )
    new = '{0}:{1}'.format(
        settings.MINIO_EXTERNAL_HOST,
        settings.MINIO_EXTERNAL_PORT
    )
    return url.replace(old, new)

