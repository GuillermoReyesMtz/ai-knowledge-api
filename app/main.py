from fastapi import FastAPI
from app.database import engine
from app.models import Base
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas import DocumentCreate
from app.schemas import DocumentResponse
from app.models import Document
from app.database import get_db
from app.models import Document
from app.database import SessionLocal
from fastapi import HTTPException
from app.services.scraper import scrape_url
from app.schemas import ScrapeRequest
from app.services.embedding_service import(
    create_embedding,
    cosine_similarity
)

Base.metadata.create_all(
    bind=engine
)

app = FastAPI()


@app.get("/")
def root():

    return {
        "message": "AI Knowledge API running"
    }

@app.post("/documents",
 response_model=DocumentResponse
 )

def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db)
):

    embedding = create_embedding(
        document.content
    )

    new_document = Document(

        title=document.title,
        content=document.content,
        embedding=embedding.tolist()
    )

    db.add(new_document)

    db.commit()

    db.refresh(new_document)

    return new_document

@app.get("/documents", 
response_model=list[DocumentResponse]
)
def get_documents(
    db: Session = Depends(get_db)
    ):

    documents = db.query(Document).all()

    return documents

@app.get("/documents/{document_id}", 
response_model=DocumentResponse
)
def get_document(document_id: int, 
db: Session = Depends(get_db)
):

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

@app.post("/scrape")
def scrape_document(payload: ScrapeRequest):

    text = scrape_url(
        payload.url
    )

    embedding = create_embedding(
        text
    )

    db = SessionLocal()

    document = Document(
        title=payload.url,
        content=text,
        embedding=embedding.tolist()
    )

    db.add(document)

    db.commit()

    db.refresh(document)

    return {
        "id": document.id,
        "message": "Document scraped"
    }

@app.get("/semantic-search")
def semantic_search(
    query: str,
    db: Session = Depends(get_db)
):

    query_embedding = create_embedding(query)

    documents = db.query(Document).all()

    results = []

    for document in documents:

        if document.embedding is None:
            continue

        score = cosine_similarity(
            query_embedding,
            document.embedding
        )

        results.append({
            "id": document.id,
            "title": document.title,
            "content": document.content,
            "score": float(score)
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return {
        "results": results[:5]
    }