from fastapi import FastAPI # type: ignore
from .bites import get_bite

app = FastAPI(title="Jargon-Free Bites Service")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Jargon-Free Bites Service!"
    }

@app.get("/bites/{feature}")
def serve_bite(feature: str):
    return {"bite": get_bite(feature)}