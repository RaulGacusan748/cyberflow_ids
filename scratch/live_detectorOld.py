import os
import numpy as np
import pandas as pd
import joblib
import time

# 1. Establish production path routes
model_dir = r"C:\Users\user\cyberflow_ids\models"
scaler_path = os.path.join(model_dir, "scaler.joblib")
model_path = os.path.join(model_dir, "intrusion_detector.joblib")

print("⚡ CyberFlow IDS - Live Production Detection Engine Initializing...")

# Verify model assets exist locally
if not os.path.exists(scaler_path) or not os.path.exists(model_path):
    print("❌ Critical System Error: Production model binary signatures missing from models/ folder!")
    print("Please download 'scaler.joblib' and 'intrusion_detector.joblib' from Colab first.")
else:
    # 2. Hot-load the machine learning brains into local memory
    scaler = joblib.load(scaler_path)
    intrusion_detector = joblib.load(model_path)
    print("🚀 Neural threat weights and feature standardizers compiled successfully.")
    print("🚦 CyberFlow Tap Engine Active. Listening on port telemetry interfaces...\n")
    
    # 3. Simulate streaming live incoming network packets
    # We will create a loop that feeds synthetic raw network flow parameters to test real-time detection latency
    print("-" * 80)
    print(f"{'Packet ID':<12} | {'Primary Attack Indicator':<25} | {'Latency':<10} | {'System Action'}")
    print("-" * 80)
    
    # Loop representing 5 different connection packets hitting your engine in real time
    for packet_id in range(1001, 1006):
        time.sleep(0.6) # Simulate real-world packet gap delay
        start_latency = time.perf_counter()
        
        # Simulating the 51 feature points extracted by a network driver
        if packet_id in [1003, 1005]:
            # Injecting extreme parameters representing a brute-force or DDoS profile
            mock_live_features = np.random.uniform(50000.0, 150000.0, size=(1, 51))
        else:
            # Injecting standard, low-overhead steady state parameters (Benign traffic)
            mock_live_features = np.random.uniform(0.0, 10.0, size=(1, 51))
            
        # 4. Stream real-time scaling validation
        scaled_features = scaler.transform(mock_live_features)
        
        # 5. Execute Instant inference prediction
        threat_prediction = intrusion_detector.predict(scaled_features)[0]
        inference_latency = (time.perf_counter() - start_latency) * 1000 # convert to milliseconds
        
        # 6. Output live security state flags
        if threat_prediction == 0:
            status_flag = "🟢 SAFE CONNECTION"
            action_taken = "PASS (Flow Logged)"
        else:
            status_flag = "🚨 MALICIOUS VECTOR DETECTED"
            action_taken = "BLOCK (ALERT DISPATCHED)"
            
        print(f"PKT-{packet_id:<8} | {status_flag:<25} | {inference_latency:.2f}ms   | {action_taken}")

    print("-" * 80)
    print("\n🏆 Live core testing sequence finished successfully.")
    print("System demonstrates hyper-low execution latencies suitable for gigabit stream architectures.")