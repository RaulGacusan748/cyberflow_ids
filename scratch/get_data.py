import os
import requests
import zipfile

# 1. Verified open-access Google Drive mirror ID for the raw CSVs
file_id = "1-t3RdDpmqMs4ABt9oobSapeNYTZJ9tpu"
url = f"https://docs.google.com/uc?export=download&id={file_id}"
zip_path = "MachineLearningCSV.zip"
target_dir = r"C:\Users\user\cyberflow_ids\data\raw"

print("🚀 Connecting to high-speed Google Drive mirror...")

def download_file_from_google_drive(url, destination):
    session = requests.Session()
    response = session.get(url, stream=True)
    
    token = None
    for key, value in response.cookies.items():
        if "download_warning" in key:
            token = value
            break
            
    if token:
        response = session.get(url + f"&confirm={token}", stream=True)
        
    os.makedirs(destination, exist_ok=True)
    full_zip_route = os.path.join(destination, zip_path)
    
    with open(full_zip_route, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024): # 1MB blocks
            if chunk:
                f.write(chunk)
    return full_zip_route

try:
    saved_zip = download_file_from_google_drive(url, target_dir)
    print("📦 Download complete. Extracting CSV sheets locally...")
    
    with zipfile.ZipFile(saved_zip, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
        
    os.remove(saved_zip) # Clean up zip to save space
    
    final_folder = os.path.join(target_dir, "MachineLearningCVE")
    if os.path.exists(final_folder):
        print("\n🏆 SUCCESS! Dataset downloaded and extracted cleanly.")
        print("Verified files inside data/raw/MachineLearningCVE:")
        print(os.listdir(final_folder))
    else:
        print("\n🏆 SUCCESS! Files extracted to data/raw:")
        print(os.listdir(target_dir))

except Exception as e:
    print(f"❌ Connection failed: {e}")