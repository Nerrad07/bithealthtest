import time
from fastapi import APIRouter, Request
from ..schemas import AddRequest, AddResponse, AskRequest, AskResponse, StatusResponse
from ..container import AppContainer

router = APIRouter()

def _container(request: Request) -> AppContainer:
    return request.app.state.container

@router.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest, request: Request):
    wf = _container(request).workflow

    start = time.perf_counter()
    result = wf.ask(payload.question)
    latency_sec = round(time.perf_counter() - start, 3)

    context_used = result.get("context_used") or result.get("hits") or []
    if isinstance(context_used, str):
        context_used = [context_used]

    answer = result.get("answer")
    if answer is None:
        if context_used:
            answer = f"I found this: '{context_used[0]}'"
        else:
            answer = "Sorry, I don't know."

    return {
        "question": payload.question,
        "answer": answer,
        "context_used": context_used,
        "latency_sec": latency_sec,
    }

@router.post("/add", response_model=AddResponse)
def add(payload: AddRequest, request: Request):
    wf = _container(request).workflow
    doc_id = wf.add(payload.text)
    return {"id": doc_id, "status": "added"}

@router.get("/status", response_model=StatusResponse)
def status(request: Request):
    c = _container(request)

    store = c.store
    store_name = type(store).__name__.lower()
    is_qdrant = "qdrant" in store_name
    is_memory = ("memory" in store_name) or ("inmemory" in store_name)

    qdrant_ready = store.is_ready() if is_qdrant else False
    in_memory_docs_count = store.count() if is_memory else 0

    return {
        "qdrant_ready": qdrant_ready,
        "in_memory_docs_count": in_memory_docs_count,
        "graph_ready": c.workflow.is_ready(),
    }
