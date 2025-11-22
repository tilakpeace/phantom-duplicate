from fastapi import FastAPI
from pydantic import BaseModel
import hashlib,json, asyncio, uuid

app=FastAPI()

# In-memory store 
submitted = {}  # It handles idempotency. For production, suggestion is to use Redis

# It maintain locking mechanism for multiple aysnc calls at same time
lock = asyncio.Lock()  


class Submission(BaseModel):
    first_name: str
    last_name: str
    address: str

def hash_payload(item: Submission) -> str:

    # create deterministic hash for deduplication
    payload_str = json.dumps(item.model_dump(), sort_keys=True)

    return hashlib.sha256(payload_str.encode()).hexdigest()



@app.post("/submit")
async def submit(item: Submission):

    payload_hash = hash_payload(item)

    # Prevent duplicates under concurrency
    async with lock:  

        # Validation -  check idempotency
        if payload_hash in submitted:
            return {
                "status": "duplicate",
                "request_id": submitted[payload_hash]["request_id"],
                "message": "Already processed",
            }

        # Submit new entry 
        request_id = str(uuid.uuid4())

        submitted[payload_hash] = {
            "request_id": request_id,
            "payload": item.dict(),
        }

        # ******Database update operation can handle here*****
        # first_name
        # last_name
        # address

        # Logging
        print(f"[LOG] Accepted request_id={request_id}, payload={item.dict()}")

    return {
        "status": "accepted",
        "request_id": request_id,
        "message": "Submission stored",
    }

