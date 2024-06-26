import uuid

from sqlalchemy import Uuid, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from main.db import Base


class Meme(Base):
    __tablename__ = 'memes'

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    img: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    bucket: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

