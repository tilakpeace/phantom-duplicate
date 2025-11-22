import requests

URL = "http://127.0.0.1:8000/submit"

payload = {
    "first_name": "Alex1",
    "last_name": "Smith",
    "address": "Germany"
}

def main():
    print("Sending first request...")
    r1 = requests.post(URL, json=payload)
    print("First response:", r1.json())

    print("\nSending second (duplicate) request...")
    r2 = requests.post(URL, json=payload)
    print("Second response:", r2.json())

    assert r1.json()["request_id"] == r2.json()["request_id"], \
        " Duplicate request should return the same request_id"
    
    print("Test passed — Idempotency works!")

if __name__ == "__main__":
    main()
