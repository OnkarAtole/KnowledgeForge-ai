from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints.documents import router as documents_router
from app.api.v1.endpoints.chat import router as chat_router


app=FastAPI(
    title="KnowledgeForge AI",
    description="AI-powered document intelligence platform",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(documents_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status":"healthy",
            "application":"KnowledgeForge AI",
            }


@app.get("/")
def root():
    return {"message":"Welcome to KnowledgeForge AI!"}





