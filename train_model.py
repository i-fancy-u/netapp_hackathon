import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

print(" Starting training...")


records = []
with open("dataset.json", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

df = pd.DataFrame(records)
print(" Loaded", len(df), "records")


df.to_csv("mock_data.csv", index=False)
print(" Converted JSON → CSV (mock_data.csv)")

#
X = df[["size_gb", "reads_last_7d", "recency_days", "latency_requirement_ms", "cost_per_gb"]]
y = df["future_tier_label"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(" Training RandomForest model...")
model = RandomForestClassifier(n_estimators=200,
    class_weight={"HOT": 3, "WARM": 1, "COLD": 1},
    random_state=42
)
model.fit(X_train, y_train)


accuracy = model.score(X_test, y_test)
print(" Model accuracy:", accuracy)


with open("storage_model.pkl", "wb") as f:
    pickle.dump(model, f)

print(" Model saved as storage_model.pkl")
