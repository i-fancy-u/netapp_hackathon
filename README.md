# Building the future of intelligent Cloud Storage

**Real-time streaming • AI-based tiering • Cloud cost reduction dashboard**

Modern cloud systems generate millions of objects, each with different access patterns and storage needs.
Storing everything in high-performance cloud storage is extremely expensive, so this system automatically classifies objects as:

| Tier | Cloud | Purpose |
|------|-------|---------|
| **HOT** | AWS High-Performance | Frequently accessed, low-latency workloads |
| **WARM** | Azure Standard | Moderately accessed storage |
| **COLD** | Glacier Deep Archive | Inactive, cheapest tier |

The dashboard shows live predictions of where each object belongs, helping reduce cloud storage bills.

---

## Features
| Feature 
|---------|
| ✅ Real-time streaming of object events |
| ✅ ML model predicts optimal tier (HOT / WARM / COLD) |
| ✅ Auto-updating Streamlit dashboard |
| ✅ KPI metrics, charts, searchable table |
| ✅ Live activity log of classification actions |
| ✅ SQLite storage for event history |
| ✅ FastAPI backend with JSON API |

---

## Tech Stack
- **Python**
- **FastAPI** – backend API
- **Streamlit** – frontend dashboard
- **SQLite** – object event database
- **Pandas** – data processing
- **Scikit-Learn** – ML model
- **Joblib** – model persistence

---

## How the ML Works
The ML classifier is trained on historical metadata:

| Feature | Meaning |
|---------|---------|
| `size_gb` | Object size in GB |
| `reads_last_7d` | Access frequency |
| `recency_days` | Days since last access |
| `latency_requirement_ms` | Performance sensitivity |
| `cost_per_gb` | Storage cost |

Using these, the model predicts which tier saves money while keeping performance acceptable.

-- In real cloud systems, the HOT storage tier is intentionally small. HOT tiers (AWS High-Performance, NVMe-backed storage) are the fastest. They are also the most expensive. And hence, our super realistic ML model makes it a reality in the simulation.

---

## Why HOT = 1, WARM = Hundreds, COLD = 0
This is realistic behavior:

- **HOT is rare** — only highly active objects qualify
- **Most objects are moderately active** → WARM
- **No object has been inactive long enough** to become COLD

✅ This means the ML model is behaving realistically — not everything becomes HOT/COLD.

---

## Why Total Sometimes Stays at 500
The system counts unique objects, not streaming events.

- The generator often reuses the same object IDs
- Their tier may change, but the object itself already exists
- So total stays constant unless a new unique object ID appears

✅ This avoids fake inflation and mirrors real cloud object storage.

---

## Folder Structure

netapp-hackathon/
│
├── backend/
│ ├── api.py # FastAPI backend
│ ├── events.db # SQLite DB storing events
│ └── generator.py # Streaming engine
│
├── ml/
│ ├── train_model.py # ML training
│ ├── storage_model.pkl # Trained model
│ └── dataset.json # Historical dataset
│
├── dashboard/
│ └── app.py # Streamlit dashboard
│
└── README.md

-- In real cloud systems, the HOT storage tier is intentionally small. HOT tiers (AWS High-Performance, NVMe-backed storage) are the fastest. They are also the most expensive. And hence, our super realistic ML model makes it a reality in the simulation.

HOW TO RUN THE PROGRAM:
1. cd ~/Projects/netapp-hackathon/streaming
python3 generator.py
(to get new objects/data in cloud)

2. cd ~/Projects/netapp-hackathon/backend
uvicorn api:app --reload --port 8000 
(to get the backend running)

3. cd ~/Projects/netapp-hackathon/dashboard
streamlit run app.py (dashboard opens at http://localhost:8501)

------------

API Root:http://127.0.0.1:8000


Objects Data:http://127.0.0.1:8000/objects


Live Logs:http://127.0.0.1:8000/logs
------------

If you get an error
❌ zsh: command not found: uvicorn

Install Uvicorn:

pip install uvicorn fastapi

Then run again:

uvicorn api:app --reload --port 8000

-----------------

[Errno 48] Address already in use

That means something else is using port 8000.

Check who is using it:

lsof -i :8000

You will see a PID (example: 12345). Kill it:

kill -9 12345


Then run backend again:

uvicorn api:app --reload --port 8000

--------------------

| Problem                        | Solution                                               |
| ------------------------------ | ------------------------------------------------------ |
| `Port 8000 already in use`     | `lsof -i :8000` → `kill -9 <PID>`                      |
| `API error: Expecting value`   | Backend is not running                                 |
| `0 objects shown`              | Generator not started                                  |
| Streamlit stuck at old numbers | Refresh or restart dashboard                           |
| HOT always 1                   | Model is correct; only highly accessed objects qualify |
| Total stuck at 500             | Because generator simulated 500 objects only           |
