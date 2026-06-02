from sqlalchemy import Column, Integer, String

from app.database import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    content = Column(
        String,
        nullable=False
    )