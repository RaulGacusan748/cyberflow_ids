# CyberFlow IDS: ML-Powered Network Anomaly Detection Framework

CyberFlow is an enterprise-grade, memory-safe network intrusion detection framework designed to ingest, process, and analyze high-velocity network flow telemetry. Using a cost-sensitive machine learning engine evaluated on the **UNB CIC-IDS2017** dataset, the system detects active threats (such as DDoS floods and automated Port Scans) in real-time, executing packet blocking actions in under 25 milliseconds.

## 🚀 Key Performance Indicators (Model Leaderboard)
| Model Paradigm | Accuracy | Precision | Recall | F1-Score | Local Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **XGBoost (Gold)** | **99.56%** | 99.10% | 98.26% | **98.68%** | N/A |
| **Random Forest (Champion)** | **99.43%** | **99.45%** | **97.16%** | **98.29%** | **~21.8 ms** |
| **Decision Tree (Silver)** | 99.21% | 98.89% | 96.43% | 97.64% | ~22.4 ms |
| **Naive Bayes (Baseline)** | 64.22% | 31.81% | **97.93%** | 48.03% | ~17.2 ms |

## 🧪 Advanced Feature Engineering
* **Packet Asymmetry**: Implemented a normalized directional ratio calculation: Asymmetry = (Fwd_Packets - Bwd_Packets) / (Fwd_Packets + Bwd_Packets + 1e-5)
* **Auto-Leakage Shield**: Dynamic correlation check to prune targets with correlations > 98%.

## 🛠️ Execution Commands
* **Run Live Tap**: python src/live_detector.py
* **Deploy FastAPI**: uvicorn src.app:app --host 0.0.0.0 --port 8000

## Submission Archive
Final submission artifacts are preserved in these folders:

* `submissions/portal_ready/` - renamed files prepared for portal upload
* `submissions/final_bundle/` - ordered archive of the core submission package
* `submissions/raw_python_code/` - raw Python source bundle for code submission

Primary portal-ready files:

* `submissions/portal_ready/Dr_Raul_C_Gacusan_CyberFlow_IDS_Assignment_Technical_Source_Code.pdf`
* `submissions/portal_ready/Dr_Raul_C_Gacusan_CyberFlow_IDS_Assignment_Final_Report.pdf`
* `submissions/portal_ready/Dr_Raul_C_Gacusan_CyberFlow_IDS_Assignment_Technical_Presentation.pptx`
* `submissions/portal_ready/Dr_Raul_C_Gacusan_CyberFlow_IDS_Assignment_Business_Presentation.pptx`

Reference for the published submission state:

* GitHub repository: https://github.com/RaulGacusan748/cyberflow_ids
* Release tag: `v1.0-submission`
