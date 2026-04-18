import csv
import pandas as pd
import os


import pandas as pd
from pathlib import Path

CSV_FILE = Path("data/cves.csv")

def save_to_csv(cves: list) -> None:
    df = pd.DataFrame(cves)
    
    if not CSV_FILE.exists():
        # soubor neexistuje - uloz s headerem
        df.to_csv(CSV_FILE, mode="w", header=True, index=False)
    else:
        # soubor existuje - pridej bez headeru
        df.to_csv(CSV_FILE, mode="a", header=False, index=False)
    
    print(f"Uloženo {len(cves)} CVEs do {CSV_FILE}")
    