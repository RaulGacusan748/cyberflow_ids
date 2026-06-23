import requests
urls = [
    "http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/MachineLearningCSV.zip",
    "http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/CIC-IDS-2017/CSVs/MachineLearningCSV.zip"
]
for url in urls:
    try:
        r = requests.get(url, stream=True)
        print("URL:", url)
        print("Status Code:", r.status_code)
        print("Headers:", {k: v for k, v in r.headers.items() if k.lower() in ["content-type", "content-length", "location"]})
        print("Preview:", r.content[:200])
        print("-" * 50)
    except Exception as e:
        print("Error for URL:", url, "-", e)
