# CyberFlow IDS EDA and Feature Engineering Report

## 1. Scope and Deliverable Mapping

This report addresses:
- Step 2: Data Collection and Understanding
- Step 3: Data Preprocessing, Applied EDA, and Feature Engineering

Reproducible assets generated:
- `reports/eda_feature_engineering_summary.json`
- `reports/data_dictionary.csv`
- `reports/shap_summary_top20.png`
- `reports/shap_bar_top20.png`
- `reports/shap_top_features.json`
- `scratch/eda_feature_engineering_report_builder.py`

## 2. Data Collection and Understanding

### 2.1 Dataset Source

- Source family: CIC-IDS-2017 derivative traffic dataset.
- Working file: `data/processed/sampled_traffic.csv`
- Record count: 126,038 rows
- Feature count: 54 columns total (53 numeric + 1 categorical)

### 2.2 Problem-Relevant Task Type

- Task type: Binary classification for intrusion detection.
- Target classes (training-aligned remap from `Label`):
  - `0`: Benign/Normal traffic
  - `1`: Attack traffic
- Distribution after remap:
  - Class `0`: 104,764
  - Class `1`: 21,274

### 2.3 Dataset Quality Summary

- Duplicate rows: 0
- Missing cells: 0
- Top missing-value columns: all zeros in top-10 summary (no missingness detected).
- Outlier evidence (IQR method): high-end outlier counts observed in timing/rate features such as `Fwd IAT Std`, `Bwd Packets/s`, `Destination Port`, and `Bwd IAT Total`.

### 2.4 Data Dictionary

A full variable-level dictionary is provided in:
- `reports/data_dictionary.csv`

Dictionary fields include:
- variable
- dtype
- missing_count
- units_or_scale
- allowed_values_or_notes
- sample_values

## 3. Data Preprocessing and Feature Engineering

### 3.1 Cleaning Pipeline

Implemented in `scratch/sample_unb_data.py` and aligned with training in `scratch/model_training_tournament.py`:
- Label column auto-detection and normalization
- Null handling: `dropna` on `Label` and numeric features
- Infinite value handling: replace `+/-inf` with `NaN`, then drop invalid rows
- Duplicate check performed in EDA summary
- Binary target remap from domain labels

### 3.2 Feature Engineering and Transformations

- Scaling: `StandardScaler` applied prior to model fitting
- Encoding: domain label-to-binary target mapping (`Label` -> `Target`)
- Metadata exclusion: non-feature columns removed (`Label`, `Target`, IP/port metadata, timestamps where present)
- Domain-derived constraints: leakage shield based on high target-correlation threshold (`|r| > 0.98`) and zero-variance feature removal

### 3.3 Applied EDA

Evidence captured in `reports/eda_feature_engineering_summary.json`:
- Class distribution
- Numeric vs categorical type profile
- Missingness profile
- IQR outlier counts by feature
- Variance/correlation-based leakage diagnostics (via training script)

## 4. Explainability, Selection, and Dimensionality Reduction

### 4.1 Feature Importance (Model-Based Explainability)

Approach used: RandomForest embedded feature importances.

Top influential features (from generated summary):
1. `Bwd Packet Length Std`
2. `Bwd Packet Length Mean`
3. `Packet Length Variance`
4. `Packet Length Std`
5. `Max Packet Length`
6. `Average Packet Size`
7. `Packet Length Mean`
8. `Bwd Packet Length Max`
9. `Total Length of Fwd Packets`
10. `Total Fwd Packets`

RandomForest validation accuracy on this analysis pass: 0.9974

### 4.1.1 SHAP Explainability (Added)

Approach used: SHAP TreeExplainer on the trained RandomForest model over a sampled test subset.

Generated SHAP outputs:
- Beeswarm-style summary plot: `reports/shap_summary_top20.png`
- Mean absolute SHAP bar plot: `reports/shap_bar_top20.png`
- Ranked top SHAP features (JSON): `reports/shap_top_features.json`

Interpretation summary:
- SHAP confirms packet-length and backward-traffic dispersion features as major contributors to threat classification.
- The SHAP ranking is consistent with model-based feature importances, strengthening explainability confidence.

### 4.2 Feature Selection Strategy

At least one method implemented (embedded/filter hybrid):
- Filter-style exclusion of zero-variance features
- Correlation-based exclusion of potential leakage proxies (`|r| > 0.98`)

This satisfies the requirement for feature selection.

### 4.3 Dimensionality Reduction (PCA)

PCA run on standardized numeric feature space:
- Features before PCA: 51
- Components needed for >=95% variance: 19
- Cumulative explained variance: 0.9506

This satisfies the dimensionality reduction requirement.

## 5. Reproducibility

To regenerate this report evidence:

```bash
python scratch/eda_feature_engineering_report_builder.py
```

Generated outputs:
- `reports/eda_feature_engineering_summary.json`
- `reports/data_dictionary.csv`
- `reports/shap_summary_top20.png`
- `reports/shap_bar_top20.png`
- `reports/shap_top_features.json`

## 6. Justification Summary

- Data quality controls (null/infinity cleaning, duplicates check, outlier profiling) reduce training instability and deployment risk.
- Leakage shield improves realism of model evaluation and avoids target-proxy inflation.
- Model-based importance provides interpretable ranking of influential traffic features.
- PCA quantifies dimensional structure and supports future compression/visual diagnostics.

## 7. Deliverable Completion Check

- [x] Dataset overview
- [x] Data dictionary
- [x] Cleaning workflow
- [x] Feature engineering workflow
- [x] Applied EDA evidence
- [x] Feature importance explainability
- [x] SHAP explainability outputs
- [x] Feature selection method
- [x] PCA dimensionality reduction
- [x] Reproducible code references
