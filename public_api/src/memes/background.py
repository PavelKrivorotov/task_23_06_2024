import json
import requests

from fastapi import UploadFile

from main.utils import get_backend_url, get_url
from main.api.private_api import settings as private_api_settings
from main.api.private_api import urls as private_api_urls

from memes.schemas import (
    ReadMeme,
    UploadMemeImage,
    UpdateMemeImage,
    DeleteMemeImage
)


private_api_base_url = get_backend_url(
    host=private_api_settings.HOST,
    port=private_api_settings.PORT
)


def get_meme_urls(memes: list[ReadMeme]) -> dict[str, str]:
    raw_urls = {}
    for meme in memes:
        raw_urls.setdefault(str(meme.id), {'bucket': meme.bucket, 'filename': meme.img})

    url = get_url(
        path=private_api_urls.List_Meme_Images,
        base_url=private_api_base_url
    )

    urls = requests.post(
        url=url,
        data=json.dumps(raw_urls),
    )

    return urls.json()

def upload_meme_image(data: UploadMemeImage, file: UploadFile):
    path = private_api_urls.Upload_Meme_Image.format(
        bucket = data.bucket,
        filename = data.filename
    )
    url = get_url(path=path, base_url=private_api_base_url)

    file = {'file': file.file.read()}

    requests.post(url=url, files=file)

def update_meme_image(data: UpdateMemeImage, file: UploadFile):
    path = private_api_urls.Update_Meme_Image.format(
        bucket = data.old_bucket,
        filename = data.old_filename
    )
    url = get_url(path=path, base_url=private_api_base_url)

    data = {
        'new_bucket': data.bucket,
        'new_filename': data.filename
    }
    file = {'file': file.file.read()}

    requests.put(url=url, data=data, files=file)

def delete_meme_image(data: DeleteMemeImage):
    path = private_api_urls.Delete_Meme_Image.format(
        bucket = data.bucket,
        filename = data.filename
    )
    url = get_url(path=path, base_url=private_api_base_url)

    requests.delete(url=url)

