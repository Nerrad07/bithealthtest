from contextlib import asynccontextmanager
from fastapi import FastAPI
from .container import AppContainer
from .api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    container = AppContainer.from_env()
    app.state.container = container
    yield
    if hasattr(container.store, "close"):
        container.store.close()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    return app

app = create_app()
