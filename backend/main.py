from fastapi import FastAPI
from database import engine, Base
from routers.upload import router as upload_router
from routers.stores import router as stores_router
from routers.traffic import router as traffic_router

app = FastAPI(title="Mall Foot Traffic API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Test basic foot traffic API running"}

app.include_router(upload_router)
app.include_router(stores_router)
app.include_router(traffic_router)