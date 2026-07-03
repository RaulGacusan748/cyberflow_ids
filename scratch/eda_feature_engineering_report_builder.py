import json
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

root = Path(r"C:\Users\user\cyberflow_ids")
path = root / "data" / "processed" / "sampled_traffic.csv"

df = pd.read_csv(path)

summary = {}
summary["rows"] = int(df.shape[0])
summary["cols"] = int(df.shape[1])
summary["duplicate_rows"] = int(df.duplicated().sum())
summary["missing_cells_total"] = int(df.isna().sum().sum())

if "Label" in df.columns:
    # Use training-aligned target mapping to ensure consistent analytics.
    df["Target"] = df["Label"].apply(lambda x: 0 if any(t in str(x).upper() for t in ["BENIGN", "NORMAL", "0"]) else 1)

summary["target_distribution"] = {str(k): int(v) for k, v in df["Target"].value_counts().to_dict().items()} if "Target" in df.columns else {}
summary["label_top10"] = {str(k): int(v) for k, v in df["Label"].value_counts().head(10).to_dict().items()} if "Label" in df.columns else {}

num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = [c for c in df.columns if c not in num_cols]
summary["numeric_col_count"] = len(num_cols)
summary["categorical_col_count"] = len(cat_cols)
summary["sample_numeric_cols"] = num_cols[:15]
summary["sample_categorical_cols"] = cat_cols[:15]

missing_by_col = df.isna().sum().sort_values(ascending=False)
summary["missing_top10"] = {str(k): int(v) for k, v in missing_by_col.head(10).to_dict().items()}

# IQR outlier counts
outlier_stats = {}
for c in num_cols:
    if c == "Target":
        continue
    s = pd.to_numeric(df[c], errors="coerce").dropna()
    if s.empty:
        continue
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    if iqr == 0:
        outliers = 0
    else:
        lo = q1 - 1.5 * iqr
        hi = q3 + 1.5 * iqr
        outliers = int(((s < lo) | (s > hi)).sum())
    outlier_stats[c] = outliers
summary["outlier_top10_iqr"] = dict(sorted(outlier_stats.items(), key=lambda kv: kv[1], reverse=True)[:10])

metadata_cols = ["Label", "Target", "Flow ID", "Source IP", "Source Port", "Destination IP", "Destination Port", "Timestamp", "Protocol"]
features_df = df.drop(columns=[c for c in metadata_cols if c in df.columns], errors="ignore")
feature_num_cols = features_df.select_dtypes(include=[np.number]).columns.tolist()
X = features_df[feature_num_cols].copy()
y = df["Target"].values

X = X.replace([np.inf, -np.inf], np.nan)
valid_idx = ~X.isna().any(axis=1)
X = X.loc[valid_idx]
y = y[valid_idx.values]

summary["model_feature_count"] = int(X.shape[1])
summary["analysis_rows_after_clean"] = int(X.shape[0])

# PCA evidence
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
pca = PCA(n_components=0.95, random_state=42)
pca.fit(X_scaled)
summary["pca_components_for_95_var"] = int(pca.n_components_)
summary["pca_explained_variance_95"] = float(pca.explained_variance_ratio_.sum())
summary["pca_first5_ratio"] = [float(x) for x in pca.explained_variance_ratio_[:5]]

# Model-based explainability via feature importances
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, stratify=y, random_state=42)
rf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
importances = rf.feature_importances_
idx = np.argsort(importances)[::-1][:15]
summary["rf_top15_importance"] = [{"feature": feature_num_cols[i], "importance": float(importances[i])} for i in idx]
summary["rf_accuracy_test"] = float(rf.score(X_test, y_test))

# SHAP explainability section (tree-based model)
X_test_df = pd.DataFrame(X_test, columns=feature_num_cols)
shap_sample_size = min(1200, len(X_test_df))
if shap_sample_size == len(X_test_df):
    X_shap = X_test_df
else:
    X_shap = X_test_df.sample(n=shap_sample_size, random_state=42)

explainer = shap.TreeExplainer(rf)
raw_shap = explainer.shap_values(X_shap)

# Handle SHAP outputs across versions/APIs.
if isinstance(raw_shap, list):
    shap_matrix = raw_shap[1] if len(raw_shap) > 1 else raw_shap[0]
elif hasattr(raw_shap, "values"):
    vals = raw_shap.values
    if vals.ndim == 3:
        shap_matrix = vals[:, :, 1]
    else:
        shap_matrix = vals
else:
    shap_matrix = raw_shap

shap_arr = np.asarray(shap_matrix)
if shap_arr.ndim == 3:
    shap_arr = shap_arr[:, :, 1]
if shap_arr.ndim == 2:
    mean_abs_shap = np.abs(shap_arr).mean(axis=0)
elif shap_arr.ndim == 1:
    mean_abs_shap = np.abs(shap_arr)
else:
    raise ValueError(f"Unexpected SHAP shape: {shap_arr.shape}")

top_shap_idx = np.argsort(mean_abs_shap)[::-1][:15].astype(int).tolist()
summary["shap_sample_size"] = int(X_shap.shape[0])
summary["shap_top15_mean_abs"] = [
    {"feature": feature_num_cols[i], "mean_abs_shap": float(mean_abs_shap[i])}
    for i in top_shap_idx
]

summary_plot_path = root / "reports" / "shap_summary_top20.png"
bar_plot_path = root / "reports" / "shap_bar_top20.png"

shap.summary_plot(shap_matrix, X_shap, max_display=20, show=False)
plt.tight_layout()
plt.savefig(summary_plot_path, dpi=150, bbox_inches="tight")
plt.close()

shap.summary_plot(shap_matrix, X_shap, plot_type="bar", max_display=20, show=False)
plt.tight_layout()
plt.savefig(bar_plot_path, dpi=150, bbox_inches="tight")
plt.close()

summary["shap_summary_plot"] = str(summary_plot_path)
summary["shap_bar_plot"] = str(bar_plot_path)

shap_rank_path = root / "reports" / "shap_top_features.json"
shap_rank_path.write_text(json.dumps(summary["shap_top15_mean_abs"], indent=2), encoding="utf-8")

out_json = root / "reports" / "eda_feature_engineering_summary.json"
out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

rows = []
for c in df.columns:
    dtype = str(df[c].dtype)
    missing = int(df[c].isna().sum())
    sample_vals = df[c].dropna().astype(str).head(5).tolist()
    allowed = ""
    units = ""
    if c == "Target":
        allowed = "0=Benign, 1=Attack"
    elif c == "Label":
        allowed = "Dataset attack family labels + normal/benign label"
    elif "Port" in c:
        units = "port number"
    elif "Duration" in c or "IAT" in c or c in ["Active Mean", "Active Max", "Active Min", "Idle Mean", "Idle Max", "Idle Min"]:
        units = "time (dataset-provided scale)"
    elif "Bytes" in c or "Length" in c or "Packet" in c:
        units = "byte/packet metric"
    elif c in ["Flow Bytes/s", "Flow Packets/s", "Fwd Packets/s", "Bwd Packets/s"]:
        units = "rate metric per second"
    rows.append({
        "variable": c,
        "dtype": dtype,
        "missing_count": missing,
        "units_or_scale": units,
        "allowed_values_or_notes": allowed,
        "sample_values": "; ".join(sample_vals),
    })

pd.DataFrame(rows).to_csv(root / "reports" / "data_dictionary.csv", index=False)
print("EDA assets generated:")
print(out_json)
print(root / "reports" / "data_dictionary.csv")
print(summary_plot_path)
print(bar_plot_path)
print(shap_rank_path)
