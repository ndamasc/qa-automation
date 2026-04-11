from fastapi import FastAPI
from api.routes import user_routes
from api.db.base import Base
from api.db.session import engine
from api.db.models.user_model import User

app = FastAPI(title="QA-API")


@app.get("/")
def health():
    return {"status": "ok"}

app.include_router(user_routes.router)