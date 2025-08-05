# wsgi.py

import threading
import uvicorn
from fastapi import FastAPI
from websocket import WebSocketApp
import json

# ====== Candle Store ======
candles = []

def add_candle(candle_data):
    if len(candles) > 1000:
        candles.pop(0)
    candles.append(candle_data)

def get_latest_candle():
    return candles[-1] if candles else None

def get_all_candles():
    return candles


# ====== WebSocket Handler ======
def on_message(ws, message):
    try:
        data = json.loads(message)
        if 'candle' in data:
            candle = {
                'time': data['candle']['timestamp'],
                'open': data['candle']['open'],
                'high': data['candle']['high'],
                'low': data['candle']['low'],
                'close': data['candle']['close']
            }
            add_candle(candle)
            print("✅ Candle Added:", candle)
    except Exception as e:
        print("⚠️ Error parsing message:", e)

def on_error(ws, error):
    print("❌ WebSocket Error:", error)

def on_close(ws, *args):
    print("🔌 WebSocket Closed")

def on_open(ws):
    print("✅ WebSocket Connected")

def start_websocket():
    ws_url = "wss://qxbroker.com/socket.io/?EIO=3&transport=websocket"  # <-- এখানে আসল URL বসাও
    ws = WebSocketApp(ws_url,
                      on_open=on_open,
                      on_message=on_message,
                      on_error=on_error,
                      on_close=on_close)
    threading.Thread(target=ws.run_forever).start()


# ====== FastAPI API Server ======
app = FastAPI(title="Qutex Real-Time Candle API")

@app.on_event("startup")
def startup_event():
    start_websocket()

@app.get("/")
def home():
    return {"message": "✅ Qutex Candle API is Running!"}

@app.get("/realtime")
def realtime():
    candle = get_latest_candle()
    return candle if candle else {"error": "No candle data yet."}

@app.get("/history")
def history():
    return get_all_candles()


# ====== Start Server from this file ======
if __name__ == "__main__":
    uvicorn.run("wsgi:app", host="0.0.0.0", port=8000, reload=True)
