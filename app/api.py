import time
from fastapi import APIRouter, HTTPException
from .schemas import QuestionRequest, DocumentRequest
from .rag_workflow import RagWorkflow

router = APIRouter()

def make_routes(workflow: RagWorkflow):
    @router.post("/ask")
    def ask_question(req: QuestionRequest):
        start = time.time()
        try:
            result = workflow.ask(req.question)
            return {
                "question": req.question,
                "answer": result["answer"],
                "context_used": result["context_used"],
                "latency_sec": round(time.time() - start, 3),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/add")
    def add_document(req: DocumentRequest):
        try:
            doc_id = workflow.add_document(req.text)
            return {"id": doc_id, "status": "added"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/status")
    def status():
        return {
            "qdrant_ready": workflow.store.is_ready(),
            "in_memory_docs_count": workflow.store.count()
            if workflow.store.__class__.__name__ == "InMemoryDocumentStore"
            else 0,
            "graph_ready": workflow.chain is not None,
        }

    return router
