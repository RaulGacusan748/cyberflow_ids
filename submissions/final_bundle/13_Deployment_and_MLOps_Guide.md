# CyberFlow IDS Deployment and MLOps Guide

## 1. Local Deployment (FastAPI)

### 1.1 Prerequisites
- Python virtual environment activated
- Required artifacts present:
  - models/scaler.joblib
  - models/intrusion_detector.joblib

### 1.2 Start API Server

```bash
c:/Users/user/cyberflow_ids/.venv/Scripts/python.exe -m uvicorn src.app:app --host 0.0.0.0 --port 8000
```

### 1.3 Test Endpoints

Health:
```bash
curl http://127.0.0.1:8000/health
```

Metadata (feature names/order):
```bash
curl http://127.0.0.1:8000/metadata
```

Predict using ordered feature array:
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.0, 1.0, 2.0]}'
```

Note: use `/metadata` to get the expected feature count and order.

## 2. Deployment Architecture

1. Input network-flow features are received through the API.
2. Features are validated and reordered to model schema.
3. StandardScaler transforms input vectors.
4. Trained model returns binary prediction (Benign/Attack).
5. API returns machine-readable JSON response.

## 3. MLOps Practices Implemented

- Artifact versioning in GitHub with release tag (`v1.0-submission`).
- Separate persisted artifacts for model and scaler.
- Reproducible training and evaluation scripts.
- Explainability artifacts (SHAP plots + top features JSON).
- Final submission bundle with traceable outputs.

## 4. Monitoring and Drift Controls (Recommended)

- Track class-wise precision/recall over time.
- Trigger retraining on sustained metric degradation.
- Log input feature distributions and compare with training baseline.
- Perform periodic leakage and schema checks before retraining.

## 5. Demo Evidence Guidance

Create a short screencast or GIF showing:
1. Starting the FastAPI server.
2. Calling `/health` and `/metadata`.
3. Calling `/predict` with one sample payload.
4. Returning a valid JSON prediction.

Suggested file name: `cyberflow_api_demo.mp4` or `cyberflow_api_demo.gif`.
