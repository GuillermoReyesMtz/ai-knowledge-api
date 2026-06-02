from pydantic import BaseModel

class DocumentCreate(BaseModel):

    title: str
    content: str


class DocumentResponse(BaseModel):

    id: int
    text: str

    class Config:
        from_attributes = True

class ScrapeRequest(BaseModel):
    url: str
    