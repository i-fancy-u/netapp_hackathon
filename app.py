import streamlit as st
import requests
import pandas as pd
import time
import random
from datetime import datetime

# ✅ Auto-refresh every 2 seconds
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()
else:
    # rerun if 2 seconds passed
    if time.time() - st.session_state.last_refresh > 2:
        st.session_state.last_refresh = time.time()
        st.experimental_rerun()


API_BASE = "http://127.0.0.1:8000"

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Smart Cloud Storage Optimizer",
    layout="wide",
)

# ------------------ GLOBAL STYLE ------------------
st.markdown("""
<style>
* {
    font-family: Arial, sans-serif !important;
}
body {
    background: linear-gradient(135deg, #052e1d 0%, #0d5b38 50%, #0c3f2a 100%) !important;
    color: #ffffff !important;
}
.big-title {
    font-size:42px !important;
    font-weight:800;
    color:#d5ffd8;
}
.subtitle {
    font-size:18px !important;
    color:#b5dbbd;
}
.metric-card {
    background: rgba(255,255,255,0.10);
    padding:20px;
    border-radius:12px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.15);
}
.metric-card img {
    margin-bottom: 8px;
}

.dataframe td {
    color: #ffffff !important;
}
.dataframe thead th {
    background-color: #1b3b2e !important;
    color: #ffffff !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("<p class='big-title'>Smart Cloud Storage Optimizer</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Real-time streaming • AI predictions • Cost-saving cloud tiering</p>", unsafe_allow_html=True)

# ------------------ CONSOLE STYLE ------------------
console_css = """
<style>
.console-box {
    background: #000000;
    padding: 18px;
    border-radius: 8px;
    color: #00ff9d;
    font-family: "Courier New", monospace;
    font-size: 15px;
    box-shadow: 0 0 10px rgba(0,255,120,0.4);
    white-space: pre-wrap;
}
</style>
"""
st.markdown(console_css, unsafe_allow_html=True)


# ------------------ LOAD DATA ------------------
try:
    resp = requests.get(f"{API_BASE}/objects")
    data = resp.json()
except Exception as e:
    st.error(f"API error: {e}")
    st.stop()

if isinstance(data, dict) and "error" in data:
    st.error(f"API returned error: {data['error']}")
    st.stop()

if not isinstance(data, list) or len(data) == 0:
    st.warning("No data returned yet.")
    st.stop()

df = pd.DataFrame.from_records(data)

if df.empty:
    st.warning("No objects found. Start streaming.")
    st.stop()


# ------------------ SEARCH BAR ------------------
search = st.text_input("🔎 Search object by ID")
if search.strip():
    df = df[df["object_id"].str.contains(search.strip(), case=False)]


# ------------------ KPI CARDS ------------------
# ---------- KPI CARDS (Clean, no icons) ----------
hot = (df["predicted_tier"] == "HOT").sum()
warm = (df["predicted_tier"] == "WARM").sum()
cold = (df["predicted_tier"] == "COLD").sum()
total = len(df)

c1, c2, c3, c4 = st.columns(4)

c1.markdown(
    f"""
    <div class="metric-card">
        <h3>HOT (AWS)</h3>
        <h1>{hot}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

c2.markdown(
    f"""
    <div class="metric-card">
        <h3>WARM (Azure)</h3>
        <h1>{warm}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

c3.markdown(
    f"""
    <div class="metric-card">
        <h3>COLD (Glacier)</h3>
        <h1>{cold}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

c4.markdown(
    f"""
    <div class="metric-card">
        <h3>Total</h3>
        <h1>{total}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------ ROW COLORING ------------------
def color_row(row):
    if row["predicted_tier"] == "HOT":
        return ['background-color: #3a2e2e'] * len(row)
    elif row["predicted_tier"] == "WARM":
        return ['background-color: #3a6b1f'] * len(row)
    elif row["predicted_tier"] == "COLD":
        return ['background-color: #2a5a89'] * len(row)
    return [''] * len(row)

# ------------------ TABLE ------------------
st.subheader("Object Tier Predictions")
st.dataframe(df.style.apply(color_row, axis=1), use_container_width=True)

# ------------------ BAR CHART ------------------
st.subheader("Tier Distribution")
st.bar_chart(df['predicted_tier'].value_counts())


# ------------------ REAL-TIME ACTIVITY LOG ------------------
st.markdown("### Activity Log")

#  styled console box
console_style = """
<style>
.log-container {
    background-color: #000000;
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 6px;
    padding: 12px;
    max-height: 200px;
    overflow-y: scroll;
    color: #00ff9d;
    font-family: 'Courier New', monospace;
    font-size: 15px;
    box-shadow: 0px 0px 10px rgba(0,255,153,0.2);
    white-space: pre-wrap;
}
</style>
"""
st.markdown(console_style, unsafe_allow_html=True)

log_box = st.empty()  # placeholder

events = [
    "Sensor stream connected",
    "New file OBJ_020 uploaded → Predicting tier...",
    "Access frequency = 55/min → Classified HOT 🔥",
    "Migrating OBJ_020 from Azure → AWS...",
    "Migration complete ✅",
    "Compressing historical logs...",
    "Moving inactive data to COLD storage ❄️",
    "Cost optimization triggered...",
    "Rebalancing storage tiers...",
]

def generate_log():
    now = datetime.now().strftime("%H:%M:%S")
    event = random.choice(events)
    return f"{now} → {event}"

# continuously refresh every 2 seconds
log_history = []

for _ in range(60):  # keeps running for many refresh cycles
    log_history.insert(0, generate_log())   # newest on top
    if len(log_history) > 12:               # keep latest 12 only
        log_history.pop()

    logs_formatted = "\n".join(log_history)
    log_box.markdown(f"<div class='log-container'>{logs_formatted}</div>", unsafe_allow_html=True)

    time.sleep(2)