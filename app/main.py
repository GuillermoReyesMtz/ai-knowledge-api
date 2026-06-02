from fastapi import FastAPI

from app.database import engine
from app.models import Base

from sqlalchemy.orm import Session
from fastapi import Depends

from app.schemas import DocumentCreate
from app.models import Document
from app.database import get_db

from app.models import Document
from app.database import SessionLocal

from fastapi import HTTPException

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

@app.get("/documents")
def get_documents():

    db = SessionLocal()

    documents = db.query(Document).all()

    return documents

@app.get("/documents/{document_id}")
def get_document(document_id: int):

    db = SessionLocal()

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document

@app.delete("/documents/{document_id}")
def delete_document(document_id: int):

    db = SessionLocal()

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted"
    }