from fastapi import FastAPI
from api.routes import user_routes
from api.db.base import Base
from api.db.session import engine

app = FastAPI(title="QA Full Pipeline API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "ok"}


app.include_router(user_routes.router)