from fastapi import APIRouter, Request
from ..schemas import AddRequest, AddResponse, AskRequest, AskResponse, StatusResponse
from ..container import AppContainer

router = APIRouter()

def _container(request: Request) -> AppContainer:
    return request.app.state.container

@router.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest, request: Request):
    wf = _container(request).workflow
    return wf.ask(payload.question)

@router.post("/add", response_model=AddResponse)
def add(payload: AddRequest, request: Request):
    wf = _container(request).workflow
    doc_id = wf.add(payload.text)
    return {"id": doc_id}

@router.get("/status", response_model=StatusResponse)
def status(request: Request):
    wf = _container(request).workflow
    return {"ready": wf.is_ready(), "count": wf.count()}