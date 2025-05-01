from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re
import signal
import sys

def handle_sigterm(signum, frame):
    print("Received SIGTERM, shutting down...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

app = Flask(__name__)

STATUS_URL = "http://127.0.0.1:8080/s2/Monitores.action"
INFO_URL = "http://127.0.0.1:8080/s2/atualizaInfo.action"

# Mapping from internal status keys to readable English names
STATUS_KEY_MAP = {
    "statusups": "ups",
    "statusbateria": "battery",
    "statusredeeletrica": "power_grid",
    "statusteste": "self_test",
    "statusalerta": "alert",
    "statusgatewaymobile": "mobile_gateway",
    "statuspotenciaelevada": "high_power"
}

@app.route('/monitor', methods=['GET'])
def get_status():
    result = {}

    # First, fetch and parse the status panels
    try:
        response = requests.get(STATUS_URL, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch status data: {str(e)}"}), 500

    soup = BeautifulSoup(response.text, 'html.parser')
    panels = soup.find_all("div", class_="col-md-4")

    status_data = {}

    for panel in panels:
        name_tag = panel.find("div", class_="nomeDigital")
        min_tag = panel.find("div", class_="DigitalMin")
        value_tag = panel.find("div", class_="DigitalValor")
        max_tag = panel.find("div", class_="DigitalMax")

        if name_tag and min_tag and value_tag and max_tag:
            raw_name = name_tag.text.strip()
            key_name = raw_name.lower().replace(" ", "_")
            min_val = min_tag.text.strip()
            value = value_tag.contents[0].strip()
            max_val = max_tag.text.strip()

            status_data[key_name] = {
                "min": min_val,
                "current": value,
                "max": max_val
            }

    result["status"] = status_data

    # Second, fetch and parse the dynamic info script
    try:
        info_response = requests.get(INFO_URL, timeout=5)
        info_response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch info data: {str(e)}"}), 500

    info_text = info_response.text

    # Extract all status changes from muda("element", "status")
    # Extract all status changes from muda("element", "status")
    status_matches = re.findall(r'muda\("([^"]+)",\s*\'([^\']+)\'\)', info_text)

    info_status = {}
    for key, value in status_matches:
        key_lower = key.lower()
        mapped_key = STATUS_KEY_MAP.get(key_lower, key_lower)
        info_status[mapped_key] = value

    # Extract shutdown time
    shutdown_match = re.search(r'\$\("#cronometroShutdown"\)\.html\("([^"]+)"\)', info_text)
    if shutdown_match:
        info_status["time_for_shutdown"] = shutdown_match.group(1)
        result["info"] = info_status

    return jsonify(result)

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000)