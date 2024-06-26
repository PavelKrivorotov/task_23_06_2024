import typing
import uuid

from fastapi import Form, File, UploadFile

from pydantic import BaseModel, ConfigDict
from pydantic import model_serializer

from main import settings
from main.utils import get_backend_url, get_url

from memes import urls as memes_urls


class BaseMeme:
    _text: str = None
    _img: UploadFile = None

    def __init__(self, text: str, img: UploadFile) -> None:
        self._text = text
        self._img = img

    @property
    def text(self) -> typing.Optional[str]:
        return self._text
    
    @property
    def img(self) -> typing.Optional[UploadFile]:
        return self._img


class WriteMeme(BaseMeme):
    def __init__(
        self,
        text: str = Form(),
        img: UploadFile = File()
    ) -> None:
        
        super().__init__(text, img)


class UpdateMeme(BaseMeme):
    def __init__(
        self,
        text: str = Form(default=None),
        img: UploadFile = File(default=None)
    ) -> None:
        
        super().__init__(text, img)


class ReadMeme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    text: str
    img: str
    bucket: str

    url: typing.Optional[str] = None

    @model_serializer
    def serializer(self) -> dict[str, str]:
        return {
            'id': str(self.id),
            'text': self.text,
            'url': self.url
        }


class ListMemes(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    result: list[ReadMeme]

    @model_serializer
    def serializer(self) -> list[ReadMeme]:
        return self.result



class BaseMemeImage(BaseModel):
    id: uuid.UUID

    @model_serializer
    def serializer(self) -> str:
        base_url = get_backend_url(
            host=settings.EXTERNAL_HOST,
            port=settings.EXTERNAL_PORT
        )
        path = memes_urls.Retrieve_Meme.format(id=self.id)
        url = get_url(path=path, base_url=base_url)
        return {'meme' : url}


class UploadMemeImage(BaseMemeImage):
    bucket: str
    filename: str


class UpdateMemeImage(UploadMemeImage):
    old_bucket: typing.Optional[str] = None
    old_filename: typing.Optional[str] = None


class DeleteMemeImage(UploadMemeImage):
    pass

