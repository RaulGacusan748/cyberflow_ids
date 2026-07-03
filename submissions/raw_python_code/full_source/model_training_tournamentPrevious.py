import os
import numpy as np
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import joblib

# 1. Define paths based on project structure
processed_file = r"C:\Users\user\cyberflow_ids\data\processed\sampled_traffic.csv"
model_save_dir = r"C:\Users\user\cyberflow_ids\models"
os.makedirs(model_save_dir, exist_ok=True)

print("🤖 CyberFlow IDS - Local Model Tournament initialized.")

if not os.path.exists(processed_file):
    print(f"❌ Error: Processed data file not found at {processed_file}")
    print("Please make sure you have successfully run scratch/sample_unb_data.py first!")
else:
    print(f"📂 Loading sampled dataset from: {processed_file}...")
    df = pd.read_csv(processed_file)
    print(f"   Successfully loaded {df.shape[0]} rows with {df.shape[1]} raw attributes.")

    # 2. Extract targets and isolate numeric features
    y = df['Target'].values
    
    # Identify non-feature metadata columns to drop if present
    metadata_cols = [
        'Label', 'Target', 'Flow ID', 'Source IP', 'Source Port', 
        'Destination IP', 'Destination Port', 'Timestamp', 'Protocol'
    ]
    
    # Drop metadata columns and filter down to strictly numeric feature sheets
    features_df = df.drop(columns=[col for col in metadata_cols if col in df.columns])
    numeric_features = features_df.select_dtypes(include=[np.number]).columns.tolist()
    
    # --- DATA LEAKAGE DIAGNOSTIC & SHIELD ENGINE ---
    print("\n🔍 Scanning feature space for data leakage or target proxies...")
    leaky_features = []
    
    for col in list(numeric_features):
        # Calculate Pearson correlation coefficient with target label
        correlation = df[col].corr(df['Target'])
        
        # Check if correlation is perfectly linear (or close to it)
        if abs(correlation) > 0.98 or np.isnan(correlation):
            leaky_features.append((col, correlation))
            
    if leaky_features:
        print("\n⚠️ WARNING: Identified potential data leakage columns!")
        print("These columns are highly correlated with the target and cause 'cheating' during training:")
        for col, corr in leaky_features:
            print(f"   - '{col}' (Correlation: {corr:.4f})")
            # Automatically filter out the leaky features to make model realistic
            if col in numeric_features:
                numeric_features.remove(col)
        print("🛡️ Leakage Shield Active: Excluded leaky columns from features to ensure a realistic evaluation.\n")
    else:
        print("✅ No direct linear leakage columns found in numeric feature space.\n")
    # ------------------------------------------------
    
    X = features_df[numeric_features].values
    print(f"⚙️ Isolated {X.shape[1]} numeric threat features for training.")

    # 3. Stratified Train/Test Split (80% Training, 20% Testing)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )
    print(f"📊 Dataset split: {X_train.shape[0]} training records, {X_test.shape[0]} validation records.")

    # 4. Standardize features to scale input variances evenly
    print("🔄 Standardizing threat vectors via StandardScaler...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save scaler instance so we can reuse it to scale live raw packet flows later
    scaler_path = os.path.join(model_save_dir, "scaler.joblib")
    joblib.dump(scaler, scaler_path)
    print(f"💾 Feature Scaler saved to {scaler_path}")

    # 5. Define Model Tournament roster
    # Keeping trees lightweight to ensure fast, memory-safe execution local-side
    tournament_models = {
        "Decision Tree": DecisionTreeClassifier(max_depth=8, min_samples_split=10, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=30, max_depth=8, random_state=42, n_jobs=-1),
        "Naive Bayes": GaussianNB()
    }

    results = []

    print("\n⚔️ Model Tournament Combat Phase Starting...\n")
    print("-" * 75)
    print(f"{'Model Name':<18} | {'Accuracy':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'Train Time':<10}")
    print("-" * 75)

    best_f1 = 0.0
    best_model_name = ""
    best_model_instance = None

    # 6. Execute Training & Validation Loop
    for name, model in tournament_models.items():
        start_time = time.time()
        
        # Train model
        model.fit(X_train_scaled, y_train)
        elapsed_time = time.time() - start_time
        
        # Test model predictions
        y_pred = model.predict(X_test_scaled)
        
        # Compute metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary')
        
        results.append({
            "model": name,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "time": elapsed_time
        })
        
        # Print iteration metric line
        print(f"{name:<18} | {accuracy:.4f}     | {precision:.4f}     | {recall:.4f}     | {f1:.4f}     | {elapsed_time:.2f}s")
        
        # Keep track of the champion classifier based on F1-Score
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model_instance = model

    print("-" * 75)

    # 7. Crown the Tournament Champion and save to disk
    champion_path = os.path.join(model_save_dir, "intrusion_detector.joblib")
    joblib.dump(best_model_instance, champion_path)
    
    print(f"\n🏆 CHAMPION CROWNED: {best_model_name.upper()} (F1-Score: {best_f1:.4f})")
    print(f"💾 Champion model successfully compiled and saved to {champion_path}!")
    print("🚦 Ready for live packet scanning pipelines!")

    # 8. Plot Performance comparison dynamically using Matplotlib & Seaborn
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        reports_dir = r"C:\Users\user\cyberflow_ids\reports"
        os.makedirs(reports_dir, exist_ok=True)
        plot_path = os.path.join(reports_dir, "model_comparison.png")
        
        print("\n📊 Generating model performance comparison visualization...")
        
        # Convert results list to DataFrame
        results_df = pd.DataFrame(results)
        
        # Melt DataFrame for Seaborn grouped bar plot
        melted_df = pd.melt(
            results_df, 
            id_vars=['model'], 
            value_vars=['accuracy', 'precision', 'recall', 'f1'],
            var_name='Metric', 
            value_name='Score'
        )
        
        # Standardize metric headers for graph legibility
        metric_map = {
            'accuracy': 'Accuracy',
            'precision': 'Precision',
            'recall': 'Recall',
            'f1': 'F1-Score'
        }
        melted_df['Metric'] = melted_df['Metric'].map(metric_map)
        
        # Set up design aesthetics
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(11, 6), dpi=150)
        
        # Draw Grouped Bar Plot
        ax = sns.barplot(
            x='Metric', 
            y='Score', 
            hue='model', 
            data=melted_df, 
            palette='viridis'
        )
        
        # Refine chart details
        plt.title('CyberFlow IDS Model Tournament - Performance Comparison', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Evaluation Metrics', fontsize=11, fontweight='bold', labelpad=10)
        plt.ylabel('Score (0.0 to 1.0)', fontsize=11, fontweight='bold', labelpad=10)
        plt.ylim(0.0, 1.1)
        plt.legend(title='Machine Learning Classifiers', loc='lower left', frameon=True)
        
        # Overlay score numbers on top of the bars
        for p in ax.patches:
            val = p.get_height()
            if val > 0:
                ax.annotate(
                    f'{val:.3f}',
                    (p.get_x() + p.get_width() / 2., val),
                    ha='center', va='center',
                    xytext=(0, 6),
                    textcoords='offset points',
                    fontsize=8,
                    fontweight='bold',
                    color='#333333'
                )
        
        plt.tight_layout()
        plt.savefig(plot_path, facecolor='white', bbox_inches='tight')
        plt.close()
        
        print(f"📈 SUCCESS! Performance comparison chart saved to:")
        print(f"   👉 {plot_path}")
        print("\n💡 View Instructions: Simply look at your Antigravity Sidebar panel, find the 'reports' folder,")
        print("   and double-click 'model_comparison.png' to display your graphs directly inside your IDE!")

    except ImportError:
        print("\n⚠️ Visualization skipped: Matplotlib and Seaborn are not installed in your local python core.")
        print("💡 Quick Fix: Run 'pip install matplotlib seaborn' to instantly enable automatic graph generation next run!")
