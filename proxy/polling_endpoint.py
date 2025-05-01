from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re
import signal
import sys
import os

def handle_sigterm(signum, frame):
    print("Received SIGTERM, shutting down...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

app = Flask(__name__)

LOGIN_URL = "http://127.0.0.1:8080/s2/checaSenha.action"
STATUS_URL = "http://127.0.0.1:8080/s2/Monitores.action"
INFO_URL = "http://127.0.0.1:8080/s2/atualizaInfo.action"

WEB_PASSWORD = os.environ.get("WEB_PASSWORD")

STATUS_ORDER = [
    "input_voltage",
    "ups_load",
    "battery_charge",
    "output_voltage",
    "output_frequency",
    "temperature"
]

STATUS_KEY_MAP = {
    "statusups": "battery_fault",
    "statusbateria": "battery_charge",
    "statusredeeletrica": "power_grid",
    "statusteste": "battery_selftest",
    "statusalerta": "alerta24h_enabled",
    "statusgatewaymobile": "mobile_server_enabled",
    "statuspotenciaelevada": "high_ups_load",
}

def login(session):
    payload = {
        "configuracoes.senha": WEB_PASSWORD
    }

    try:
        response = session.post(LOGIN_URL, data=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        return False, f"Login request failed: {str(e)}"

    if "msgErro" in response.text:
        return False, "Invalid password"

    return True, None

@app.route('/monitor', methods=['GET'])
def get_status():
    result = {}

    session = requests.Session()

    # Authenticate if WEB_PASSWORD is provided
    if WEB_PASSWORD:
        success, error = login(session)
        if not success:
            return jsonify({"error": error}), 401

    try:
        response = session.get(STATUS_URL, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch status data: {str(e)}"}), 500

    soup = BeautifulSoup(response.text, 'html.parser')
    panels = soup.find_all("div", class_="col-md-4")

    status_data = {}

    for idx, panel in enumerate(panels):
        if idx >= len(STATUS_ORDER):
            break

        key_name = STATUS_ORDER[idx]

        min_tag = panel.find("div", class_="DigitalMin")
        value_tag = panel.find("div", class_="DigitalValor")
        max_tag = panel.find("div", class_="DigitalMax")

        if min_tag and value_tag and max_tag:
            min_val = min_tag.text.strip()
            value = value_tag.contents[0].strip()
            max_val = max_tag.text.strip()

            status_data[key_name] = {
                "min": min_val,
                "current": value,
                "max": max_val
            }

    result["status"] = status_data

    try:
        info_response = session.get(INFO_URL, timeout=5)
        info_response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch info data: {str(e)}"}), 500

    info_text = info_response.text

    status_matches = re.findall(r'muda\("([^"]+)",\s*\'([^\']+)\'\)', info_text)

    info_status = {}
    for key, value in status_matches:
        key_lower = key.lower()
        mapped_key = STATUS_KEY_MAP.get(key_lower, key_lower)
        info_status[mapped_key] = value

    shutdown_match = re.search(r'\$\("#cronometroShutdown"\)\.html\("([^"]+)"\)', info_text)
    if shutdown_match:
        info_status["time_for_shutdown"] = shutdown_match.group(1)

    result["info"] = info_status

    return jsonify(result)

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000)