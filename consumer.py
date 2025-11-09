from paho.mqtt import client as mqtt
import json
import sqlite3

conn = sqlite3.connect("events.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    object_id TEXT,
    read_increment INTEGER,
    size_gb REAL,
    recency_days INTEGER,
    latency_requirement_ms INTEGER,
    cost_per_gb REAL
)
""")
conn.commit()

def on_message(client, userdata, msg):
    e = json.loads(msg.payload.decode())

    
    ts  = e.get("timestamp")
    oid = e.get("object_id")
    ri  = int(e.get("read_increment", 0))
    sz  = float(e.get("size_gb", 0.0))
    rd  = int(e.get("recency_days", 0))
    lat = int(e.get("latency_requirement_ms", 0))
    cost= float(e.get("cost_per_gb", 0.0))

    cur.execute("""
        INSERT INTO events (timestamp, object_id, read_increment, size_gb, recency_days, latency_requirement_ms, cost_per_gb)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (ts, oid, ri, sz, rd, lat, cost))
    conn.commit()
    print("💾 Saved:", oid, ri, sz, rd, lat, cost)

BROKER = "broker.hivemq.com"
TOPIC = "netapp/streaming/events"

cli = mqtt.Client()
cli.connect(BROKER, 1883)
cli.subscribe(TOPIC)
cli.on_message = on_message

print("✅ Consumer listening + storing…")
cli.loop_forever()
