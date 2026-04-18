# CVE Analyzer

Automatizovaný nástroj pro stahování a analýzu CVE (Common Vulnerabilities and Exposures) dat z NVD databáze.

## Co projekt dělá

Stahuje aktuální CVE záznamy z NVD API, ukládá je lokálně a provádí analytické vizualizace pro pochopení trendů v kybernetické bezpečnosti.

## Architektura
NVD API → nvd_client.py → csv_storage.py → data/cves.csv
↓
analysis.ipynb

## Tech stack

- **Python** – hlavní jazyk
- **Pandas** – analýza dat
- **Matplotlib / Seaborn** – vizualizace
- **NVD API** – zdroj CVE dat

## Jak spustit

1. Nainstaluj závislosti:
```bash
pip install -r requirements.txt
```

2. Stáhni CVE data:
```bash
python ingest.py
```

3. Otevři analytický notebook:
notebook/analysis.ipynb

## Co analyzuje

- Distribuce CVEs podle severity (CRITICAL, HIGH, MEDIUM, LOW)
- Top 10 nejčastějších typů zranitelností (CWE)
- Pokrytí záplatami (patch coverage)
- Trend publikovaných CVEs v čase

## Struktura projektu
ve-analyzer/
├── src/
│   ├── nvd_client.py      # stahování a parsování z NVD API
│   ├── state_manager.py   # incremental loading
│   ├── csv_storage.py     # ukládání do CSV
│   └── cwe_client.py      # CWE popisky od MITRE
├── notebook/
│   └── analysis.ipynb     # analytické vizualizace
├── ingest.py              # vstupní bod
└── requirements.txt

