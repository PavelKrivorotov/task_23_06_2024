from fastapi import Depends, Path
from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from main.db import get_db
from main.validators import Re_UUID_Validator
from memes.models import Meme


def get_meme_id_or_error(
    id: str = Path(pattern=Re_UUID_Validator),
    db: Session = Depends(get_db)
) -> str:
    
    query = select(
        select(Meme)
        .where(Meme.id == id)
        .exists()
    )
    state = db.scalar(query)

    if not state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return id

