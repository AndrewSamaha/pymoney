# main.py

from fastapi import FastAPI
from app.routes.all_transactions import router as api_router

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        log_level="info",
        reload=True,
    )