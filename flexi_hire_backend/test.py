import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'serviceAccountKey.json')

try:
    with open(FIREBASE_CREDENTIALS_PATH) as f:
        service_account_info = json.load(f)
    print("success")
    print(json.dumps(service_account_info, indent=4))  # Pretty print
except Exception as e:
    print("not success")
    print("Error:", e)
