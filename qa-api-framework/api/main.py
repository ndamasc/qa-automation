from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routes import user_routes
from api.db.base import Base
from api.db.session import engine
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="QA-API",
    description="A secure and organized API for user management",
    version="1.0.0",
    lifespan=lifespan  # 👈 aqui
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler (com debug)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()  # 👈 debug real
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

@app.get("/")
def health():
    return {"status": "ok"}

app.include_router(user_routes.router)