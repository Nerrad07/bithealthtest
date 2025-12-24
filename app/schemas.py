from pydantic import BaseModel, Field

class AddRequest(BaseModel):
    text: str = Field(..., min_length=1)

class AddResponse(BaseModel):
    id: int
    status: str

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)

class AskResponse(BaseModel):
    question: str
    answer: str
    context_used: list[str]
    latency_sec: float

class StatusResponse(BaseModel):
    qdrant_ready: bool
    in_memory_docs_count: int
    graph_ready: bool
