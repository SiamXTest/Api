# api_server.py
from fastapi import FastAPI
from candles_store import get_latest_candle, get_all_candles
from websocket_client import start_websocket

app = FastAPI(title="Qutex Real-Time Candle API", version="1.0")

@app.on_event("startup")
def start_ws():
    start_websocket()

@app.get("/")
def home():
    return {"message": "🚀 Qutex Candle API is running!"}

@app.get("/realtime")
def realtime():
    candle = get_latest_candle()
    return candle if candle else {"error": "No candle data yet."}

@app.get("/history")
def history():
    return get_all_candles()py
