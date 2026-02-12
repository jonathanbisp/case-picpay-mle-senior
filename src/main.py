from fastapi import FastAPI
import os
from pymongo import MongoClient

app = FastAPI(title="PicPay Case API")

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)  # type: ignore
db = client.get_database()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items")
def list_items():
    return {"count": db.items.count_documents({})}
