import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Configuration
BASE_URL = "http://localhost:5000/api/v1"
DATA_FILE = "data.json"
MAX_WORKERS = 10  # Adjust based on server capacity

def send_ipn(item):
    provider_code = item['providerCode']
    payload = item['payload']
    url = f"{BASE_URL}/{provider_code}"
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        return {
            "provider": provider_code,
            "status_code": response.status_code,
            "response": response.json(),
            "success": response.status_code == 200
        }
    except Exception as e:
        return {
            "provider": provider_code,
            "error": str(e),
            "success": False
        }

def main():
    print(f"Loading data from {DATA_FILE}...")
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {DATA_FILE} not found. Please run generate_data.py first.")
        return

    print(f"Starting test for {len(data)} records using {MAX_WORKERS} workers...")
    
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Map the send_ipn function across the data list
        results = list(executor.map(send_ipn, data))
    
    end_time = time.time()
    
    # Summary
    total = len(results)
    successes = sum(1 for r in results if r.get('success'))
    failures = total - successes
    
    print("\n" + "="*30)
    print("IPN TEST SUMMARY")
    print("="*30)
    print(f"Total Requests: {total}")
    print(f"Success (200 OK): {successes}")
    print(f"Failures: {failures}")
    print(f"Time Taken: {end_time - start_time:.2f} seconds")
    print(f"Avg Req/Sec: {total / (end_time - start_time):.2f}")
    print("="*30)

    # Print a few sample errors if they exist
    if failures > 0:
        print("\nSample Failures:")
        fail_samples = [r for r in results if not r.get('success')]
        for s in fail_samples[:5]:
            print(f"Provider: {s.get('provider')} | Error: {s.get('error') or s.get('status_code')}")

if __name__ == "__main__":
    main()
