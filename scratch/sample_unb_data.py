import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# 1. Define local path structure
raw_dir = r"C:\Users\user\cyberflow_ids\data\raw"
output_dir = r"C:\Users\user\cyberflow_ids\data\processed"
output_file = os.path.join(output_dir, "sampled_traffic.csv")

os.makedirs(output_dir, exist_ok=True)

# Find any CSV file inside the raw directory
csv_files = [f for f in os.listdir(raw_dir) if f.lower().endswith('.csv') and not f.startswith('.')]

if not csv_files:
    print(f"❌ No CSV files found in {raw_dir}. Please make sure your UNB file is placed there!")
else:
    target_csv = os.path.join(raw_dir, csv_files[0])
    print(f"🎯 Target raw dataset identified: {target_csv}")
    print("🔍 Inspecting file format and layout characteristics...")
    
    try:
        # Detect delimiter and clean BOM/weird encoding characters
        with open(target_csv, 'r', encoding='utf-8-sig', errors='ignore') as f:
            first_line = f.readline()
            
        separator = ';' if (';' in first_line and first_line.count(';') > first_line.count(',')) else ','
        print(f"ℹ️ Auto-detected column separator: '{separator}'")
        
        # Read the first row to inspect columns safely
        preview = pd.read_csv(target_csv, sep=separator, nrows=1, encoding='utf-8-sig')
        preview.columns = preview.columns.str.strip().str.replace('"', '').str.replace("'", "")
        
        print(f"📋 First 5 columns found: {list(preview.columns[:5])}")
        
        # Robust label matching dictionary
        possible_labels = ['label', 'class', 'category', 'threat', 'attack', 'target', 'type']
        detected_label_col = None
        
        for col in preview.columns:
            cleaned_col_name = str(col).strip().lower()
            if any(term == cleaned_col_name or term in cleaned_col_name for term in possible_labels):
                detected_label_col = col
                break
                
        if detected_label_col:
            print(f"🎯 Successfully matched classification column: '{detected_label_col}'")
        else:
            print("\n❌ ERROR: Could not locate a matching threat classification column.")
            print("Here are all the columns found in your file so we can map them:")
            print(list(preview.columns))
            raise KeyError("No suitable label column detected.")

        print("\n🔄 Initializing chunk-by-chunk downsampling & quality cleansing (Memory Safe)...")
        sampled_chunks = []
        chunk_size = 100000  # Process in memory-safe chunks
        
        for i, chunk in enumerate(pd.read_csv(target_csv, sep=separator, chunksize=chunk_size, low_memory=False, encoding='utf-8-sig')):
            # Standardize columns
            chunk.columns = chunk.columns.str.strip().str.replace('"', '').str.replace("'", "")
            
            # Rename matched column to standard 'Label'
            chunk = chunk.rename(columns={detected_label_col: 'Label'})
            
            # Drop empty label records
            chunk = chunk.dropna(subset=['Label'])
            
            # Map benign vs attack classes
            chunk['Target'] = chunk['Label'].apply(lambda x: 0 if str(x).strip().upper() in ['BENIGN', '0', 'NORMAL'] else 1)
            
            # Isolate numerical features to clean them
            numeric_cols = chunk.select_dtypes(include=[np.number]).columns.tolist()
            if 'Target' in numeric_cols:
                numeric_cols.remove('Target')
                
            # Replace infinities and drop null calculation errors
            chunk[numeric_cols] = chunk[numeric_cols].replace([np.inf, -np.inf], np.nan)
            chunk = chunk.dropna(subset=numeric_cols)
            
            # Extract a stratified 5% slice
            if len(chunk) > 10:
                try:
                    _, sub_sample = train_test_split(
                        chunk, 
                        test_size=0.05, 
                        stratify=chunk['Target'], 
                        random_state=42
                    )
                    sampled_chunks.append(sub_sample)
                except ValueError:
                    # Fallback to standard random sample if class ratios are too skewed in this chunk
                    sampled_chunks.append(chunk.sample(frac=0.05, random_state=42))
            
            print(f"   Processed chunk {i+1}...")

        if not sampled_chunks:
            raise ValueError("No valid data rows could be parsed or cleaned.")

        # Combine, save, and print validation stats
        final_sample_df = pd.concat(sampled_chunks, ignore_index=True)
        final_sample_df.to_csv(output_file, index=False)
        
        print("\n🏆 SUCCESS! Your balanced and cleaned mini-dataset is ready.")
        print(f"💾 File saved to: {output_file}")
        print(f"📊 Dimensions: {final_sample_df.shape[0]} rows, {final_sample_df.shape[1]} features")
        print("\nDistribution of traffic classes in your sampled file:")
        print(final_sample_df['Label'].value_counts())

    except Exception as e:
        print(f"❌ Processing failed: {e}")
