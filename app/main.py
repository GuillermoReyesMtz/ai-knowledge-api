from fastapi import FastAPI

from app.database import engine
from app.models import Base

from sqlalchemy.orm import Session
from fastapi import Depends

from app.schemas import DocumentCreate
from app.models import Document
from app.database import get_db

Base.metadata.create_all(
    bind=engine
)

app = FastAPI()


@app.get("/")
def root():

    return {
        "message": "AI Knowledge API running"
    }

@app.post("/documents")
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db)
):

    new_document = Document(

        title=document.title,
        content=document.content
    )

    db.add(new_document)

    db.commit()

    db.refresh(new_document)

    return new_document