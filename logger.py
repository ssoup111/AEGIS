import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("logs/decisions.jsonl")
LOG_PATH.parent.mkdir(exist_ok=True)

def log_decision(decision: dict):
    record = dict(decision)
    record["timestamp"] = datetime.now().isoformat()
    with LOG_PATH.open("a") as f:
        f.write(json.dumps(record) + "\n")
