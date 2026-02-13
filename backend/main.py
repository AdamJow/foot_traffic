from fastapi import FastAPI
from database import engine, Base

app = FastAPI(title="Mall Foot Traffic API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Test Mall Foot Traffic API running"}