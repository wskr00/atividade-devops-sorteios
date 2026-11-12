import json
import logging
import os
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request

VERSION = "1.0.0"
app = FastAPI(title="API de Sorteios", version=VERSION)
logger = logging.getLogger("sorteios")
logger.setLevel(logging.INFO)
logger.propagate = False
if not logger.handlers:
    logger.addHandler(logging.StreamHandler(sys.stdout))
    if log_file := os.getenv("LOG_FILE"):
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        logger.addHandler(logging.FileHandler(log_file, encoding="utf-8"))


@app.middleware("http")
async def log_request(request: Request, call_next):
    start = time.perf_counter()
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        logger.info(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "method": request.method,
            "route": request.url.path,
            "status": status,
            "duration_ms": round((time.perf_counter() - start) * 1000, 2),
            "version": VERSION,
        }, ensure_ascii=False))


@app.get("/")
def index():
    return {"nome": "API de Sorteios", "versao": VERSION}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/sortear")
def sortear(minimo: int = Query(1, alias="min"), maximo: int = Query(100, alias="max")):
    if minimo > maximo:
        raise HTTPException(status_code=400, detail="min deve ser menor ou igual a max")
    return {"numero": random.randint(minimo, maximo), "min": minimo, "max": maximo}
