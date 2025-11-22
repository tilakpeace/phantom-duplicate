# MVP Project shows mechanism for phantom-duplicate

This MVP project demonstrates true idempotency handling, ensuring consistent behavior even under multiple simultaneous connections and identical requests.

### Solution
1) Locking mechanism 
3) Idempotency key handle

### Api operation
* Submit


## Project Setup

#### Command for project setup 

* python -m venv venv 
* source venv/bin/activate
* pip install -r requirements.txt
* Run command: uvicorn main:app --reload 
* Access url : http://127.0.0.1:8000/submit

#### Command to handle test runs
* Open three seperate terminals 
* In first terminal, run command: uvicorn main:app --reload 

* In second terminal, run command: python test_requests.py
* In third terminal, run command: python test_concurrency.py  



## Overview

This document provides information on the available API endpoints, including their purpose, request formats, and response structures.

---

## Base URL

```
http://127.0.0.1:8000
```

---

## Endpoints

### 1. **Transaction Submit**

**POST** `/submit`

#### **Request Body (JSON)**

```json
{
    "first_name":"Alex1",
    "last_name":"Smith1",
    "address":"Germany"

}
```

#### **Response for unique transaction**

```json
{
    "status": "accepted",
    "request_id": "2991437c-b5e8-4679-a151-a6c96e0db294",
    "message": "Submission stored"
}
```

#### **Response for duplicate transaction**

```json
{
    "status": "duplicate",
    "request_id": "2991437c-b5e8-4679-a151-a6c96e0db294",
    "message": "Already processed"
}
```


---