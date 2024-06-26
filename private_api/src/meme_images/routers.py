from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.responses import Response, JSONResponse

from meme_images.schemas import (
    WriteImage,
    UpdateImage,
    DeleteImage,
    ReadImage,
    ListImages
)
from meme_images.crud import meme_images_crud


router = APIRouter()


@router.post('/images')
def list_images(data: dict[str, ReadImage]) -> JSONResponse:
    res = ListImages(images=data).model_dump()
    return JSONResponse(content=res)


@router.post('/images/{bucket}/{filename}/upload')
def upload_image(data: WriteImage = Depends()) ->JSONResponse:
    url = meme_images_crud.upload_image(data)
    return JSONResponse(
        content = {'url': url},
        status_code=status.HTTP_201_CREATED
    )


@router.put('/images/{bucket}/{filename}')
def update_image(data: UpdateImage = Depends()) -> JSONResponse:
    url = meme_images_crud.update_image(data)
    return JSONResponse(
        content = {'url': url},
        status_code=status.HTTP_202_ACCEPTED
    )


@router.delete('/images/{bucket}/{filename}')
def delete_image(data: DeleteImage = Depends()) -> Response:
    meme_images_crud.delete_image(data)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

