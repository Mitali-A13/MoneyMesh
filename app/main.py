from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import user
from app.routes import user_routes

app = FastAPI(title="Finance Backend API")

# routes
app.include_router(user_routes.router)

# create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API is running"}
