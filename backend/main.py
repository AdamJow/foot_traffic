import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers.upload import router as upload_router
from routers.stores import router as stores_router
from routers.traffic import router as traffic_router

app = FastAPI(title="Mall Foot Traffic API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(upload_router)
app.include_router(stores_router)
app.include_router(traffic_router)

# Serve react frontend
frontend_dist_path = os.path.join(os.path.dirname(__file__), "dist")

if os.path.exists(frontend_dist_path):

    # Serve static assets like JS/CSS
    app.mount(
        "/assets",
        StaticFiles(directory=os.path.join(frontend_dist_path, "assets")),
        name="assets",
    )

    # Catch all route to serve index.html for SPA
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        return FileResponse(os.path.join(frontend_dist_path, "index.html"))
