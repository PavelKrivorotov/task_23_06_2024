import datetime
import uuid

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from memes.models import Meme
from memes.schemas import (
    WriteMeme,
    UpdateMeme,
    ReadMeme,
    ListMemes,
    UploadMemeImage,
    UpdateMemeImage,
    DeleteMemeImage
)
from memes.filters import ListMemesFilter
from memes.utils import make_bucket_name, make_object_name


class MemesCRUD:
    def list_memes(self, db: Session, filter: ListMemesFilter) -> ListMemes:
        c_query = select(func.count(Meme.id))
        count = db.scalar(c_query)

        if filter.offset >= count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No more memes!'
            )
        
        m_query = (
            select(Meme)
            .limit(filter.limit)
            .offset(filter.offset)
            .order_by(Meme.id)
        )
        memes = db.scalars(m_query)
        return ListMemes(result=memes.all())

    def retrieve_meme(self, db: Session, meme_id: str) -> ReadMeme:
        meme = db.get(Meme, meme_id)
        return ReadMeme.model_validate(meme)

    def create_meme(self, db: Session, data: WriteMeme) -> UploadMemeImage:
        meme_id = uuid.uuid4()
        filename = make_object_name(data.img.filename)
        bucket = make_bucket_name(datetime.datetime.now())

        meme = Meme(
            id=meme_id,
            text=data.text,
            img=filename,
            bucket=bucket
        )
        db.add(meme)
        db.commit()

        return UploadMemeImage(
            id=meme_id,
            bucket=bucket,
            filename=filename
        )

    def update_meme(
        self,
        db: Session,
        data: UpdateMeme,
        meme_id: str
    ) -> UpdateMemeImage:
        
        old_img_values = {}
        values = {}
        
        if data.text:
            values.setdefault('text', data.text)

        if data.img:
            old_meme = db.get(Meme, meme_id)
            old_img_values.setdefault('bucket', old_meme.bucket)
            old_img_values.setdefault('filename', old_meme.img)

            values.setdefault('img', make_object_name(data.img.filename))
            values.setdefault('bucket', make_bucket_name(datetime.datetime.now()))

        if values:
            query = (
                update(Meme)
                .where(Meme.id == meme_id)
                .values(values)
                .returning(Meme)
            )
            meme = db.scalar(query)
            db.commit()
            db.refresh(meme)

            return UpdateMemeImage(
                id=meme.id,
                bucket=meme.bucket,
                filename=meme.img,
                old_bucket=old_img_values.get('bucket'),
                old_filename=old_img_values.get('filename')
            )

    def delete_meme(self, db: Session, meme_id: str) -> DeleteMemeImage:
        meme = db.get(Meme, meme_id)
        old_bucket = meme.bucket
        old_filename = meme.img

        db.delete(meme)
        db.commit()

        return DeleteMemeImage(
            id=meme.id,
            bucket=old_bucket,
            filename=old_filename
        )

memes_crud = MemesCRUD()

