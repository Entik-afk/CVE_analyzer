import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import time
STATE_FILE = Path("data/state.json")

class StateManager:
    def __init__(self,):
        self.state_file = STATE_FILE
        
    def load_state(self) -> dict:
        if self.state_file.exists():
            with open(self.state_file, "r") as f:
                return json.load(f)
        else:
            return {
                "last_updated": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%S.000"),
                "total_cves": 0,
                "last_run_status": "none"
            }
    def save_state(self, total_cves:int, status: str):
        # aktualizujeme stavový soubor
        state = {
            "last_updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000"),
            "total_cves": total_cves,
            "last_run_status": status
        }
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)
        
