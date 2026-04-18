from src.nvd_client import NVDClient
from src.state_manager import StateManager
from datetime import datetime
from src.csv_storage import save_to_csv
from pathlib import Path


def main():
    Path("data").mkdir(parents=True, exist_ok=True)
    state_manager = StateManager()
    state = state_manager.load_state()
    last_updated = datetime.strptime(state["last_updated"], "%Y-%m-%dT%H:%M:%S.000")
    print(f"Stahuji od: {last_updated}")

    nvd_client = NVDClient()
    
    try:
        new_cves = nvd_client.fetch_cves(last_updated, datetime.now())
        save_to_csv(new_cves)
        state_manager.save_state(total_cves=len(new_cves), status="success")
        print(f"Staženo {len(new_cves)} CVEs")
    except Exception as e:
        state_manager.save_state(total_cves=0, status="failed")
        print(f"Chyba při stahování: {e}")

if __name__ == "__main__":
    main()