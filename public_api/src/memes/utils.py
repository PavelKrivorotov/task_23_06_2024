import datetime
import secrets

from main import settings


def make_bucket_name(now: datetime.datetime) -> str:
    return now.strftime('%Y-%m-%d')

def make_object_name(filename: str) -> str:
    name, extension = filename.split('.')
    salt = secrets.token_urlsafe(settings.BUCKET_OBJECT_SALT)

    return '{name}_{salt}.{extension}'.format(
        name=name,
        salt=salt,
        extension=extension
    )

