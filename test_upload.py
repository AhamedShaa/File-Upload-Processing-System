import requests
import json

API_URL = "https://t8hvn4leel.execute-api.us-east-1.amazonaws.com"

# Step 1 — Get presigned URL from API
response = requests.post(
    f"{API_URL}/upload",
    json={
        "filename":    "A.Ahamed.jpg",
        "contentType": "image/jpeg"
    }
)

body   = response.json()
job_id = body['jobId']

print(f"Job ID: {job_id}")
print(f"Uploading...")

# Step 2 — Upload directly to S3
with open(r'C:\Users\MSI\Desktop\A.Ahamed.jpg', 'rb') as f:
    upload_response = requests.put(
        body['uploadUrl'],
        data=f,
        headers={'Content-Type': 'image/jpeg'}
    )

print(f"Upload status: {upload_response.status_code}")

# Step 3 — Check job status
import time
time.sleep(5)  # wait for processing

status_response = requests.get(f"{API_URL}/status/{job_id}")
print(f"Job status: {json.dumps(status_response.json(), indent=2)}")