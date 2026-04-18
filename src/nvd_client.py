import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import time

NVD_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
STATE_FILE = Path("data/state.json")

# Vytvoření klienta pro NVD API
class NVDClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.headers = {}
        
        if api_key:
            self.headers["apiKey"] = api_key

    def fetch_cves(self, start_date: datetime, end_date: datetime) -> list:
        all_cves = []
        start_index = 0
        page_size = 2000  # Maximální počet záznamů na stránku

        while True:
            params = {
                "pubStartDate": start_date.strftime("%Y-%m-%dT%H:%M:%S.000") + "Z",
                "pubEndDate": end_date.strftime("%Y-%m-%dT%H:%M:%S.000") + "Z",
                "startIndex": start_index,
                "resultsPerPage": page_size
            }
            
            data = self._make_request(params)
            print(f"API response: {data}") 
            cves = data.get("vulnerabilities", [])

            # místo extend - parsujeme každý záznam
            for raw_cve in cves:
                parsed = self._parse_cve(raw_cve)
                all_cves.append(parsed)

            total = data.get("totalResults", 0)
            start_index += page_size

            if start_index >= total:
                break
        return all_cves

    def _parse_cve(self, raw_cve: dict) -> dict:
        cve = raw_cve.get("cve", {})
        
        # základní info
        cve_id = cve.get("id", "")
        published = cve.get("published", "")
        last_modified = cve.get("lastModified", "")
        
        # popis - chceme jen anglický
        descriptions = cve.get("descriptions", [])
        description = next(
            (d["value"] for d in descriptions if d["lang"] == "en"),
            "No description available"
        )
        
        # CVSS score - může být v31 nebo v30
        metrics = cve.get("metrics", {})
        cvss_data = (
            metrics.get("cvssMetricV31", [{}])[0].get("cvssData", {})
            or metrics.get("cvssMetricV30", [{}])[0].get("cvssData", {})
        )
        score = cvss_data.get("baseScore", None)
        severity = cvss_data.get("baseSeverity", "UNKNOWN")
        vector = cvss_data.get("vectorString", "")
        
        # CWE typ zranitelnosti
        weaknesses = cve.get("weaknesses", [])
        cwe = next(
            (w["description"][0]["value"] 
            for w in weaknesses 
            if w.get("description")),
            "UNKNOWN"
        )
        
        # má patch?
        references = cve.get("references", [])
        has_patch = any(
            "Patch" in ref.get("tags", []) 
            for ref in references
        )
        
        return {
            "cve_id": cve_id,
            "published": published,
            "last_modified": last_modified,
            "description": description,
            "cvss_score": score,
            "severity": severity,
            "cvss_vector": vector,
            "cwe": cwe,
            "has_patch": has_patch
        }


    def _make_request(self, params: dict) -> dict:
        max_retries = 5
        wait_time = 1  # Počáteční čekací doba v sekundách

        for attempt in range(max_retries):
            response = requests.get(
                NVD_BASE_URL,
                headers=self.headers,
                params=params
            )
            print(f"Status code: {response.status_code}") 
            print(f"URL: {response.url}")

            if response.status_code == 200:
                print(f"Status code: {response.status_code}") 
                return response.json()
            
            
            
            elif response.status_code == 429:
                print(f"Rate limit hit, čekám {wait_time} sekund...")
                print(f"Status code: {response.status_code}") 
                time.sleep(wait_time)
                wait_time *= 2  # exponential backoff
            
            elif response.status_code == 403:
                print(f"Status code: {response.status_code}") 
                raise Exception("Špatný API klíč nebo nemáš přístup")
                p
            
            elif response.status_code >= 500:
                print(f"Server error {response.status_code}, zkouším znovu...")
                print(f"Status code: {response.status_code}") 
                time.sleep(wait_time)
                wait_time *= 2

        raise Exception(f"Neúspěšný pokus o získání dat po {max_retries} pokusech")


