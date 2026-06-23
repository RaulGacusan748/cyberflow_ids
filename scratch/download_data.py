import os
import requests
import zipfile

url = "http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/CIC-IDS-2017/CSVs/MachineLearningCSV.zip"
zip_path = "MachineLearningCSV.zip"
target_dir = r"C:\Users\user\cyberflow_ids\data\raw"

print("Connecting to Canadian Institute for Cybersecurity (CIC) mirror...")

def download_file(url, destination):
    os.makedirs(destination, exist_ok=True)
    full_zip_route = os.path.join(destination, zip_path)
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(full_zip_route, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024): # 1MB blocks
            if chunk:
                f.write(chunk)
    return full_zip_route

try:
    # Execute the streaming download
    saved_zip = download_file(url, target_dir)
    print("Download complete. Extracting CSV sheets locally...")
    
    # Extract the zip file safely using native python tools
    with zipfile.ZipFile(saved_zip, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
        
    os.remove(saved_zip) # Remove the installer zip to free up disk space
    
    # Final Architecture Structural Validation Check
    final_folder = os.path.join(target_dir, "MachineLearningCVE")
    if os.path.exists(final_folder):
        print("\nSUCCESS! Dataset downloaded and extracted cleanly.")
        print(f"Verified files inside {final_folder}:")
        print(os.listdir(final_folder))
    else:
        print(f"Files extracted to {target_dir} but subfolder naming differs.")
        print(os.listdir(target_dir))

except Exception as e:
    print(f"Connection failed: {e}")
