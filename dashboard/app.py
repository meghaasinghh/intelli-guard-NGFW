"""
Priya — Flask Dashboard + REST API
Run: python dashboard/app.py
Serves the admin UI and exposes API endpoints for all modules.
"""
from flask import Flask, jsonify, render_template
import pandas as pd, os

app = Flask(__name__, template_folder="templates", static_folder="static")

LOG_PATH = "data/logs/firewall_audit.csv"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/logs")
def get_logs():
    if not os.path.exists(LOG_PATH):
        return jsonify([])
    df = pd.read_csv(LOG_PATH).tail(200)
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/stats")
def get_stats():
    if not os.path.exists(LOG_PATH):
        return jsonify({
            "total": 0, "blocked": 0, "allowed": 0, "alerts": 0, "latency_avg": 0.0,
            "protocols": {}, "sources": {}, "top_attackers": {}
        })
    df = pd.read_csv(LOG_PATH)
    latency_avg = float(df["latency_ms"].mean()) if "latency_ms" in df and len(df) > 0 else 0.0
    if pd.isna(latency_avg):
        latency_avg = 0.0
        
    protocols = df["proto"].value_counts().to_dict() if "proto" in df else {}
    sources = df["source"].value_counts().to_dict() if "source" in df else {}
    
    # Top 5 blocked IPs
    top_attackers = {}
    if "verdict" in df and "src_ip" in df:
        top_attackers = df[df["verdict"] == "BLOCK"]["src_ip"].value_counts().head(5).to_dict()

    return jsonify({
        "total":   len(df),
        "blocked": int((df["verdict"] == "BLOCK").sum()) if "verdict" in df else 0,
        "allowed": int((df["verdict"] == "ALLOW").sum()) if "verdict" in df else 0,
        "alerts":  int((df["verdict"] == "ALERT").sum()) if "verdict" in df else 0,
        "latency_avg": round(latency_avg, 2),
        "protocols": protocols,
        "sources": sources,
        "top_attackers": top_attackers
    })

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    import yaml
    try:
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
        port = config["dashboard"]["port"]
    except Exception:
        port = 5001
        
    app.run(host="0.0.0.0", port=port, debug=False)
