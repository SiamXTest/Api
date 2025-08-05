# websocket_client.py
import websocket
import threading
import json
from candles_store import add_candle

def on_message(ws, message):
    # এখানে Candle data parse করে save করতে হবে (dummy format নিচে)
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
    ws_url = "wss://qxbroker.com/socket.io/?EIO=3&transport=websocket"  # এখানে আসল WebSocket URL বসাও
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    threading.Thread(target=ws.run_forever).start()
