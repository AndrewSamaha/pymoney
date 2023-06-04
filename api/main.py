# main.py

from fastapi import FastAPI
from app.routes.all_transactions import router as api_router
from app.routes.health_check import router as health_check_router
from app.routes.summary import router as summary_router

app = FastAPI()

app.include_router(health_check_router, prefix="")
app.include_router(api_router, prefix="/api/v1")
app.include_router(summary_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        log_level="info",
        reload=True,
    )