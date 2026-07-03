import pandas as pd
from fastapi.testclient import TestClient
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.app import app


def main() -> None:
    with TestClient(app) as client:
        health = client.get('/health')
        meta = client.get('/metadata')

        if health.status_code != 200:
            raise RuntimeError(f'Health check failed: {health.text}')

        meta_json = meta.json()
        feature_cols = meta_json.get('feature_columns', [])

        df = pd.read_csv('data/processed/sampled_traffic.csv')
        row = df.iloc[0]

        payload = {'feature_map': {c: float(row[c]) for c in feature_cols}}
        pred = client.post('/predict', json=payload)

        print('HEALTH:', health.json())
        print('FEATURE_COUNT:', len(feature_cols))
        print('PREDICT:', pred.json())


if __name__ == '__main__':
    main()
