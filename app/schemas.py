from pydantic import BaseModel, Field

class AddRequest(BaseModel):
    text: str = Field(..., min_length=1)

class AddResponse(BaseModel):
    id: int

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)

class AskResponse(BaseModel):
    question: str
    context: str
    hits: list[str]

class StatusResponse(BaseModel):
    ready: bool
    count: int
