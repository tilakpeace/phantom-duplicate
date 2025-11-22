import requests
import concurrent.futures

URL = "http://127.0.0.1:8000/submit"

payload = {
    "first_name": "Alex",
    "last_name": "Smith",
    "address": "Germany"
}

def send_request():
    return requests.post(URL, json=payload).json()

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda _: send_request(), range(10)))

    print("\n=== Responses ===")
    for r in results:
        print(r)

    # Count accepted vs duplicate
    accepted = [r for r in results if r["status"] == "accepted"]
    duplicates = [r for r in results if r["status"] == "duplicate"]

    assert len(accepted) == 1, "❌ Exactly ONE request must be accepted"
    assert len(duplicates) == 9, "❌ All other requests must be duplicates"

    # Check they all share the same request_id
    request_ids = {r["request_id"] for r in results}
    assert len(request_ids) == 1, "❌ All request_id should be identical"

    print("\n✅ Concurrency test passed! Idempotency lock works.")

if __name__ == "__main__":
    main()
