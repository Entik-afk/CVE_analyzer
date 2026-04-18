import requests
import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO

CWE_URL = "https://cwe.mitre.org/data/xml/cwec_latest.xml.zip"

def fetch_cwe_names() -> dict:
    # stahneme zipovany XML soubor
    response = requests.get(CWE_URL)
    
    # rozbalime zip
    with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
        xml_filename = zip_file.namelist()[0]
        xml_file = zip_file.read(xml_filename)
    
    # parsujeme XML
    root = ET.fromstring(xml_file)
    
    # vytvorime slovnik
    cwe_names = {}
    for cwe in root.findall(".//{http://cwe.mitre.org/cwe-7}Weakness"):
        cwe_id = cwe.get("ID")
        cwe_name = cwe.get("Name")
        if cwe_id and cwe_name:
            cwe_names[f"CWE-{cwe_id}"] = cwe_name
    
    return cwe_names