import json

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_and_health():
    assert client.get("/").json() == {"nome": "API de Sorteios", "versao": "1.0.0"}
    assert client.get("/health").json() == {"status": "ok"}


def test_sortear_valid():
    assert client.get("/sortear?min=7&max=7").json()["numero"] == 7
    result = client.get("/sortear").json()
    assert 1 <= result["numero"] <= 100
    assert result["min"] == 1 and result["max"] == 100
    assert -10 <= client.get("/sortear?min=-10&max=-1").json()["numero"] <= -1


def test_invalid_parameters():
    assert client.get("/sortear?min=10&max=1").status_code == 400
    assert client.get("/sortear?min=abc").status_code == 422


def test_request_log(caplog):
    # The app logger does not propagate, so capture its own handler.
    from app.main import logger
    import logging
    records = []
    class Capture(logging.Handler):
        def emit(self, record):
            records.append(json.loads(record.getMessage()))
    handler = Capture()
    logger.addHandler(handler)
    try:
        client.get("/sortear?min=2&max=1")
    finally:
        logger.removeHandler(handler)
    event = records[-1]
    assert event["route"] == "/sortear" and event["status"] == 400
    assert event["method"] == "GET" and event["duration_ms"] >= 0
    assert event["timestamp"] and event["version"]
