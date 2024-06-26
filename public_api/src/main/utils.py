from main import settings


def get_backend_url(
        http_protocol: str = settings.HTTP_PROTOCOL,
        host: str = settings.HOST,
        port: str = settings.PORT
) -> str:
    
    return '{0}://{1}:{2}'.format(
        http_protocol,
        host,
        port
    )

base_url = get_backend_url()


def get_url(path: str = '/', base_url: str = base_url) -> str:
    return '{0}{1}'.format(base_url, path)

