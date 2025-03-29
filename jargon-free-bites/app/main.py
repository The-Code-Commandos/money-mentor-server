from fastapi import FastAPI # type: ignore
from .bites import get_bite

app = FastAPI(title="Jargon-Free Bites Service")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Jargon-Free Bites Service!"
    }

@app.get("/bites/{feature}")
def serve_bite(feature: str, subkey: str = None, fear: str = None):
    feature_bites = get_bite(feature)
    print(f"Feature_bites: {feature_bites}")
    
    if isinstance(feature_bites, str):
        return {"bite": f"{feature} is your easy money buddy—try it!"}
    
    # Return specific subkey if provided, else whole dict
    if subkey and subkey in feature_bites:
        bite_dict = feature_bites[subkey]
        bite = bite_dict.get(fear) if fear and fear in bite_dict else bite_dict["default"]
        return {"bite": bite}
    return {"bites": feature_bites}