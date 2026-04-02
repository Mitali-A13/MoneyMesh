from fastapi import FastAPI
from app.db.database import engine, Base

app = FastAPI(title="Finance Backend API")

# create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API is running"}
