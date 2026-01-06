from fastapi import FastAPI
from app.api.endpoints import router as resume_routers
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.config import create_tables
from app.account.routers import router as account_routers

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_tables()
    yield

app = FastAPI(
    title="Resume IQ",
    description="ATS based resume scoring and matching using NLP and LLM",
    version="1.0.0",
    lifespan=lifespan
)

# To connect React and FastAPI, React must call the backend using the full API URL consisting of the backend base URL and the API routing path. 
# Frontend routing and backend routing are completely separate and should not be mixed.
app.add_middleware(
     CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_routers)
app.include_router(resume_routers)