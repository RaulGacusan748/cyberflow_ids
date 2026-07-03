# CyberFlow IDS Final Report

## Cover Page

**Project:** CyberFlow IDS

**Author:** [Your Name]

**Program/Course:** [Program and Course]

**Institution:** [Institution Name]

**Date:** [Submission Date]

**Repository Link:** https://github.com/RaulGacusan748/cyberflow_ids

**Google Colab Link:** [Paste your shareable Colab URL here]

---

## Abstract

CyberFlow IDS is an intrusion detection workflow that combines cybersecurity traffic preprocessing, supervised model tournament evaluation, and live replay-based inference to classify benign and malicious traffic patterns. This project demonstrates reproducible model selection and practical deployment outputs for both technical and non-technical stakeholders.

---

## 1. Introduction

Network intrusion detection remains essential as enterprise environments continue to generate high-volume, heterogeneous traffic. Signature-only approaches can miss novel attacks, motivating machine learning models that can generalize from behavioral indicators.

This project proposes an end-to-end IDS pipeline named CyberFlow IDS, designed to:
- preprocess cleaned CIC-IDS-2017 derived data,
- evaluate multiple models under a consistent training protocol,
- select the strongest model via leaderboard metrics,
- support a dashboard and a terminal replay workflow for demonstration.

---

## 2. Objectives

- Build a reproducible machine learning IDS pipeline.
- Compare candidate classifiers in a tournament framework.
- Validate the selected model on held-out traffic data.
- Demonstrate practical usability through dashboard and replay simulation.

---

## 3. Related Work and Context

Traditional IDS systems include signature-based and anomaly-based methods. Machine learning IDS expands anomaly detection by learning multi-feature traffic behavior and enabling higher adaptability.

[Add your literature review summary and citations here.]

---

## 4. Dataset and Preprocessing

### 4.1 Dataset Source

- Primary dataset family: CIC-IDS-2017 derivatives.
- Working input file path in this project:
  - data/raw/cicids2017_cleaned.csv

### 4.2 Preparation Steps

- Data cleaning and label normalization.
- Feature selection / exclusion of unsupported fields.
- Numerical scaling with persistent scaler serialization.
- Train/validation split for tournament evaluation.

[Add specific preprocessing decisions from your scripts here.]

---

## 5. Methodology

### 5.1 Model Tournament Strategy

Candidate models are trained under consistent data partitions and compared by performance metrics (e.g., accuracy, precision, recall, F1, ROC-AUC where applicable).

### 5.2 Winner Selection

A leaderboard ranks candidate models. The top model is serialized as production artifact for downstream inference.

[Insert exact winning model and metrics from your logs.]

---

## 6. Implementation

### 6.1 Training Engine

- Core file: scratch/model_training_tournament.py
- Output artifacts:
  - models/intrusion_detector.joblib
  - models/scaler.joblib

### 6.2 Dashboard

- Core file: src/dashboard.py
- Purpose: interactive traffic analytics and prediction interface.

### 6.3 Live Replay Detector

- Core file: scratch/live_detector.py
- Purpose: terminal-based simulation/replay and real-time style classification output.

---

## 7. Results

[Insert model tournament leaderboard screenshot/table and key metrics.]

[Insert validation discussion, error patterns, and confusion analysis.]

---

## 8. Discussion

- Strengths: reproducibility, clear tournament comparison, deployable artifacts.
- Limitations: dataset bias, class imbalance, and environment-specific generalization limits.
- Practical implications for SOC workflows and triage support.

---

## 9. Conclusion and Future Work

CyberFlow IDS demonstrates an operational machine learning IDS workflow from data preparation to deployable inference components. Future work can include online learning, drift monitoring, and broader benchmark datasets.

---

## References

[Add references in your required citation style.]

---

## Appendix (Optional)

- Terminal logs excerpt
- Architecture diagram
- Additional evaluation charts
