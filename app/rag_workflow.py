from langgraph.graph import StateGraph, END
from .stores.base import DocumentStore
from .services.embedding import EmbeddingService

class RagWorkflow:
    def __init__(self, store: DocumentStore, embedder: EmbeddingService):
        self.store = store
        self.embedder = embedder
        self.chain = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(dict)
        workflow.add_node("retrieve", self._retrieve)
        workflow.add_node("answer", self._answer)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)
        return workflow.compile()

    def _retrieve(self, state: dict) -> dict:
        query = state["question"]
        vec = self.embedder.embed(query)
        state["context"] = self.store.search(query, vec, limit=2)
        return state

    def _answer(self, state: dict) -> dict:
        ctx = state.get("context", [])
        if ctx:
            state["answer"] = f"I found this: '{ctx[0][:100]}...'"
        else:
            state["answer"] = "Sorry, I don't know."
        return state

    def ask(self, question: str) -> dict:
        result = self.chain.invoke({"question": question})
        return {
            "answer": result["answer"],
            "context_used": result.get("context", []),
        }

    def add_document(self, text: str) -> int:
        vec = self.embedder.embed(text)
        return self.store.add(text, vec)
