from pathlib import Path
from typing import Dict, List, Optional

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, model_validator

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"
DATA_PATH = ROOT / "data" / "processed" / "sampled_traffic.csv"

SCALER_PATH = MODELS_DIR / "scaler.joblib"
MODEL_PATH = MODELS_DIR / "intrusion_detector.joblib"

METADATA_COLS = {
    "Label",
    "Target",
    "Flow ID",
    "Source IP",
    "Source Port",
    "Destination IP",
    "Destination Port",
    "Timestamp",
    "Protocol",
}


class PredictRequest(BaseModel):
    # Option A: ordered list of 51 numeric features.
    features: Optional[List[float]] = Field(default=None, description="Ordered numeric feature list")
    # Option B: map of feature name -> value; server will reorder to model feature order.
    feature_map: Optional[Dict[str, float]] = Field(default=None, description="Feature map keyed by feature name")

    @model_validator(mode="after")
    def validate_payload(self):
        if self.features is None and self.feature_map is None:
            raise ValueError("Provide either 'features' or 'feature_map'.")
        return self


app = FastAPI(
    title="CyberFlow IDS API",
    description="Local deployment API for CyberFlow intrusion detection",
    version="1.0.0",
)


@app.on_event("startup")
def startup_load_assets():
    if not SCALER_PATH.exists() or not MODEL_PATH.exists():
        raise RuntimeError("Model artifacts are missing in models/ directory.")

    app.state.scaler = joblib.load(SCALER_PATH)
    app.state.model = joblib.load(MODEL_PATH)

    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
        feature_cols = [c for c in df.columns if c not in METADATA_COLS]
        feature_cols = [c for c in feature_cols if pd.api.types.is_numeric_dtype(df[c])]
        app.state.feature_cols = feature_cols
    else:
        app.state.feature_cols = []


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": True,
        "feature_count": len(app.state.feature_cols),
    }


@app.get("/metadata")
def metadata():
    return {
        "feature_count": len(app.state.feature_cols),
        "feature_columns": app.state.feature_cols,
    }


@app.post("/predict")
def predict(payload: PredictRequest):
    feature_cols = app.state.feature_cols

    if payload.features is not None:
        x = np.array(payload.features, dtype=float).reshape(1, -1)
    else:
        if not feature_cols:
            raise HTTPException(status_code=400, detail="Feature schema unavailable. Use 'features' ordered list.")
        missing = [c for c in feature_cols if c not in payload.feature_map]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing feature keys: {missing[:10]}")
        x = np.array([payload.feature_map[c] for c in feature_cols], dtype=float).reshape(1, -1)

    expected = app.state.scaler.n_features_in_
    if x.shape[1] != expected:
        raise HTTPException(status_code=400, detail=f"Expected {expected} features, received {x.shape[1]}.")

    x_scaled = app.state.scaler.transform(x)
    pred = int(app.state.model.predict(x_scaled)[0])

    return {
        "prediction": pred,
        "label": "Attack" if pred == 1 else "Benign",
    }
