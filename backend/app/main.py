from app.db import session
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import db_manager

settings = settings()

@asynccontextmanager
async def lifespan(app:FastAPI):
    await db_manager.connect_to_database(settings.MONGODB_URL)
    yield
    await db_manager.close_database_connection()

app =  FastAPI(
    title= settings.PROJECT_NAME,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health",tags=["Health"])
async def health_check() ->dict[str,str] :
    return {"status":"Ok"}