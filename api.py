from fastapi import FastAPI
import sqlite3
import pandas as pd
import joblib
import numpy as np
from datetime import datetime

logs = []

def add_log(message: str):
    now = datetime.now().strftime("%H:%M:%S")
    logs.append(f"{now} → {message}")




app = FastAPI()


model = joblib.load("../ml/storage_model.pkl")

@app.get("/logs")
def get_logs():
    return logs[-10:]

@app.get("/")
def home():
    return {"message": "Backend running"}


@app.get("/objects")
def get_objects():
    try:
       
        conn = sqlite3.connect("events.db")
        df = pd.read_sql_query("SELECT * FROM events", conn)
        conn.close()

        if df.empty:
            return []

        
        if "read_increment" in df.columns:
            df = df.rename(columns={"read_increment": "reads_last_7d"})

        
        feature_order = [
            "size_gb",
            "reads_last_7d",
            "recency_days",
            "latency_requirement_ms",
            "cost_per_gb",
        ]

      
        for col in feature_order:
            if col not in df.columns:
                df[col] = 0

        
        X = df[feature_order].astype(float)

       
        preds = model.predict(X)
        df["predicted_tier"] = preds

        
        for obj, tier in zip(df["object_id"], df["predicted_tier"]):
            if tier == "HOT":
                add_log(f"Object {obj} classified HOT 🔥 — Moving to AWS High-Performance")
            elif tier == "WARM":
                add_log(f"Object {obj} classified WARM — Stored on Azure Standard")
            else:
                add_log(f"Object {obj} classified COLD ❄️ — Archived to Glacier Deep Archive")

        df = df.replace([np.inf, -np.inf, np.nan], 0)

        return df.to_dict(orient="records")

    except Exception as e:
        add_log(f" Backend error: {e}")
        return {"error": str(e)}


    
logs = []

def add_log(message: str):
    from datetime import datetime
    now = datetime.now().strftime("%H:%M:%S")
    logs.append(f"{now} → {message}")

@app.get("/logs")
def get_logs():
    return logs[-10:]  

