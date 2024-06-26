from fastapi import Form, Path, File, UploadFile

from pydantic import BaseModel
from pydantic import model_serializer

from main.minio import client
from meme_images.utils import replace_host


class BaseImage:
    def __init__(
        self,
        bucket: str = Form(),
        filename: str = Form(),
    ) -> None:
        
        self._bucket = bucket
        self._filename = filename

    @property
    def bucket(self) -> str:
        return self._bucket
    
    @property
    def filename(self) -> str:
        return self._filename


class WriteImage(BaseImage):
    def __init__(
        self,
        bucket: str = Path(),
        filename: str = Path(),
        file: UploadFile = File()
    ) -> None:
        
        super().__init__(bucket, filename)
        self._file = file

    @property
    def file(self) -> UploadFile:
        return self._file


class UpdateImage(WriteImage):
    def __init__(
        self,
        bucket: str = Path(),
        filename: str = Path(),
        new_bucket: str = Form(),
        new_filename: str = Form(),
        file: UploadFile = File()
    ) -> None:
        
        super().__init__(new_bucket, new_filename, file)
        self._old_bucket = bucket
        self._old_filename = filename

    @property
    def old_bucket(self) -> str:
        return self._old_bucket
    
    @property
    def old_filename(self) -> str:
        return self._old_filename


class DeleteImage(BaseImage):
    def __init__(
        self,
        bucket: str = Path(),
        filename: str = Path()
    ) -> None:
        
        super().__init__(bucket, filename)


class ReadImage(BaseModel):
    bucket: str
    filename: str

    @model_serializer
    def serializer(self) -> str:
        url = client.get_presigned_url(
            method='GET',
            bucket_name=self.bucket,
            object_name=self.filename
        )
        return replace_host(url)


class ListImages(BaseModel):
    images: dict[str, ReadImage]

    @model_serializer
    def serializer(self) -> dict[str, ReadImage]:
        return self.images
    
