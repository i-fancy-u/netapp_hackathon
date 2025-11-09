import json
import time
import random
from datetime import datetime
from paho.mqtt import client as mqtt

# ---- CONFIG ----
BROKER = "broker.hivemq.com"
TOPIC = "netapp/streaming/events"
PUBLISH_INTERVAL_SEC = 2

# a small pool of object IDs
OBJECT_IDS = [f"OBJ_{i:04d}" for i in range(1, 21)]

# helper to generate mixed-realistic values (Option C)
def make_event():
    obj_id = random.choice(OBJECT_IDS)

    # timestamp (this is what was missing before)
    ts = datetime.utcnow().isoformat()

    # reads: skewed so some are hot bursts, many are low
    read_inc = max(0, int(random.gauss(mu=6, sigma=4)))

    # size: log-normalish spread (0.1 GB to ~100 GB)
    size_gb = round(max(0.1, random.lognormvariate(0.0, 1.0) * 5), 2)

    # recency_days: more recent is more common
    recency_days = max(0, int(random.expovariate(1/3)))  # 0..~15 typical

    
    latency_requirement_ms = random.choices(
        population=[5, 10, 20, 50, 100, 200],
        weights=[20, 20, 20, 15, 15, 10],
        k=1
    )[0]

    
    cost_per_gb = random.choices(
        population=[0.02, 0.05, 0.10, 0.20],
        weights=[25, 35, 25, 15],
        k=1
    )[0]

    return {
        "timestamp": ts,
        "object_id": obj_id,
        "read_increment": read_inc,
        "size_gb": size_gb,
        "recency_days": recency_days,
        "latency_requirement_ms": latency_requirement_ms,
        "cost_per_gb": cost_per_gb,
    }

def main():
    client = mqtt.Client()
    client.connect(BROKER, 1883)
    print(f" MQTT Streaming → {BROKER} topic={TOPIC}")

    try:
        while True:
            event = make_event()
            client.publish(TOPIC, json.dumps(event))
            print(" Sent:", event)
            time.sleep(PUBLISH_INTERVAL_SEC)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
