import copy

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.responses import Response, JSONResponse
from fastapi.background import BackgroundTasks

from sqlalchemy.orm import Session

from main.db import get_db

from memes import background
from memes.depends import get_meme_id_or_error
from memes.schemas import WriteMeme, UpdateMeme
from memes.crud import memes_crud
from memes.filters import ListMemesFilter


router = APIRouter()


@router.get('/memes')
def list_memes(
    filter: ListMemesFilter = Depends(),
    db: Session = Depends(get_db)
) -> JSONResponse:

    memes = memes_crud.list_memes(db, filter)
    urls = background.get_meme_urls(memes.result)

    for meme in memes.result:
        meme.url = urls.get(str(meme.id))

    return JSONResponse(content=memes.model_dump())


@router.get('/memes/{id}')
def retrieve_meme(
    id: str = Depends(get_meme_id_or_error),
    db: Session = Depends(get_db)
) -> JSONResponse:

    meme = memes_crud.retrieve_meme(db, id)
    url = background.get_meme_urls([meme])
    meme.url = url.get(str(meme.id))

    return JSONResponse(content=meme.model_dump())


@router.post('/memes')
def create_meme(
    background_tasks: BackgroundTasks,
    data: WriteMeme = Depends(),
    db: Session = Depends(get_db),
) -> JSONResponse:

    meme = memes_crud.create_meme(db, data)
    background_tasks.add_task(
        func=background.upload_meme_image,
        data=meme,
        file=copy.deepcopy(data.img)
    )

    return JSONResponse(
        content=meme.model_dump(),
        status_code=status.HTTP_201_CREATED
    )


@router.put('/memes/{id}')
def update_meme(
    background_tasks: BackgroundTasks,
    id: str = Depends(get_meme_id_or_error),
    data: UpdateMeme = Depends(),
    db: Session = Depends(get_db)
) -> JSONResponse:

    meme = memes_crud.update_meme(db, data, id)

    if data.img:
        background_tasks.add_task(
            func=background.update_meme_image,
            data=meme,
            file=copy.deepcopy(data.img)
        )

    return JSONResponse(
        content=meme.model_dump(),
        status_code=status.HTTP_202_ACCEPTED
    )


@router.delete('/memes/{id}')
def delete_meme(
    background_tasks: BackgroundTasks,
    id: str = Depends(get_meme_id_or_error),
    db: Session = Depends(get_db)
) -> JSONResponse:

    meme = memes_crud.delete_meme(db, id)
    background_tasks.add_task(
        func=background.delete_meme_image,
        data=meme
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

