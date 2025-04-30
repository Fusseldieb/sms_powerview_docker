from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

SOURCE_URL = "http://127.0.0.1:8080/s2/Monitores.action"

@app.route('/monitor', methods=['GET'])
def get_status():
    try:
        response = requests.get(SOURCE_URL, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500

    soup = BeautifulSoup(response.text, 'html.parser')
    panels = soup.find_all("div", class_="col-md-4 medidor")
    result = {}

    for panel in panels:
        name_tag = panel.find("div", class_="nomeDigital")
        min_tag = panel.find("div", class_="DigitalMin")
        value_tag = panel.find("div", class_="DigitalValor")
        max_tag = panel.find("div", class_="DigitalMax")

        if name_tag and min_tag and value_tag and max_tag:
            name = name_tag.text.strip()
            min_val = min_tag.text.strip()
            value = value_tag.text.strip()
            max_val = max_tag.text.strip()

            result[name] = {
                "min": min_val,
                "current": value,
                "max": max_val
            }

    return jsonify(result)

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000)