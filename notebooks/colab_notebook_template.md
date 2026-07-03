# CyberFlow IDS Colab Notebook Template

Use this template to build your Google Colab notebook for submission.

Instructor-friendly structure:
- Add a Markdown cell before each Code cell.
- Keep the heading format exactly as shown so checking is easier.
- Include short notes about purpose, input, and output.

## Cell 1 - Project Setup

### Documentation (Markdown cell before Code Cell 1)

**Purpose:** Import required libraries and verify runtime readiness.

**Input:** None.

**Output:** A confirmation message that the environment is ready.

```python
# CyberFlow IDS - Colab Setup
from pathlib import Path
import joblib
import pandas as pd
import numpy as np

print('Environment ready')
```

## Cell 2 - Upload or Mount Data

### Documentation (Markdown cell before Code Cell 2)

**Purpose:** Define where the dataset is located and optionally connect Google Drive.

**Input:** Dataset file path.

**Output:** Printed data path used in the notebook.

```python
# Option A: upload files manually in Colab UI
# Option B: mount Google Drive if your files are stored there

from google.colab import drive
# drive.mount('/content/drive')

DATA_PATH = '/content/cicids2017_cleaned.csv'  # change path as needed
print('Data path set to:', DATA_PATH)
```

## Cell 3 - Load Dataset

### Documentation (Markdown cell before Code Cell 3)

**Purpose:** Load the traffic dataset into a pandas DataFrame.

**Input:** CSV file at `DATA_PATH`.

**Output:** Dataset shape and first five rows for quick inspection.

```python
df = pd.read_csv(DATA_PATH)
print('Shape:', df.shape)
df.head()
```

## Cell 4 - Load Trained Artifacts

### Documentation (Markdown cell before Code Cell 4)

**Purpose:** Load the trained IDS model and scaler for inference.

**Input:** Serialized files (`intrusion_detector.joblib`, `scaler.joblib`).

**Output:** Loaded model objects and readiness confirmation.

```python
# Upload these files in Colab before running:
# - intrusion_detector.joblib
# - scaler.joblib

MODEL_PATH = '/content/intrusion_detector.joblib'
SCALER_PATH = '/content/scaler.joblib'

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
print('Model and scaler loaded')
```

## Cell 5 - Prepare Features

### Documentation (Markdown cell before Code Cell 5)

**Purpose:** Separate features and labels, then scale features using the saved scaler.

**Input:** Loaded dataset and correct target column name.

**Output:** Scaled feature matrix for prediction.

```python
# Update this block to match your actual training feature columns and target label name.
TARGET_COL = 'Label'  # change if needed

X = df.drop(columns=[TARGET_COL])
y = df[TARGET_COL]

X_scaled = scaler.transform(X)
print('Prepared features:', X_scaled.shape)
```

## Cell 6 - Run Predictions

### Documentation (Markdown cell before Code Cell 6)

**Purpose:** Generate class predictions using the trained model.

**Input:** Scaled feature matrix `X_scaled`.

**Output:** Predicted labels (`y_pred`) and total prediction count.

```python
y_pred = model.predict(X_scaled)
print('Predictions generated:', len(y_pred))
```

## Cell 7 - Basic Evaluation

### Documentation (Markdown cell before Code Cell 7)

**Purpose:** Report performance statistics for model validation.

**Input:** Ground-truth labels `y` and predictions `y_pred`.

**Output:** Classification report and confusion matrix.

```python
from sklearn.metrics import classification_report, confusion_matrix

print(classification_report(y, y_pred))
print(confusion_matrix(y, y_pred))
```

## Cell 8 - Save Sample Output

### Documentation (Markdown cell before Code Cell 8)

**Purpose:** Build a quick comparison table of actual vs predicted labels.

**Input:** `y` and `y_pred`.

**Output:** Preview table for qualitative checking.

```python
out = pd.DataFrame({'actual': y, 'predicted': y_pred})
out.head(20)
```

## Submission Notes

- Run all cells successfully before sharing.
- Click Share in Colab and set access to Anyone with the link can view.
- Paste the Colab link in your final report cover page.
- Keep both markdown explanations and code cells in the final notebook.
