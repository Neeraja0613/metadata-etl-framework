from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

data = [
    {"id":1,"name":"API1","last_modified":"2024-01-01T00:00:00"},
    {"id":2,"name":"API2","last_modified":"2024-01-02T00:00:00"},
    {"id":3,"name":"API3","last_modified":"2024-01-03T00:00:00"}
]

@app.get("/data")
def get_data(since: str = None):
    if since:
        return [d for d in data if d["last_modified"] > since]
    return data