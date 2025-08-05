# candles_store.py
candles = []

def add_candle(candle_data):
    if len(candles) > 1000:  # পুরাতন ডেটা ক্লিন করতে চাইলে
        candles.pop(0)
    candles.append(candle_data)

def get_latest_candle():
    return candles[-1] if candles else None

def get_all_candles():
    return candles
