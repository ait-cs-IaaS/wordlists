import requests
import json
import csv
from datetime import datetime


def transform_country_json(json_data):
    return [{"value": name, "category": "Country"} for code, name in json_data.items()]


def get_countries():
    url = "http://country.io/names.json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors

        json_data = response.json()
        transformed_data = sorted(transform_country_json(json_data), key=lambda x: x["value"])

        result_data = {
            "version": 1,
            "data": [
                {
                    "name": "Countries",
                    "description": f"List of countries {datetime.now().isoformat()}",
                    "usage": 4,
                    "link": "https://raw.githubusercontent.com/ait-cs-IaaS/wordlists/master/output/countries.json",
                    "entries": transformed_data,
                }
            ],
        }

        with open("output/countries.json", "w") as output_file:
            json.dump(result_data, output_file, indent=4, ensure_ascii=False)

        print(f"Saved {len(transformed_data)} entries to output/countries.json successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def transform_austrian_municipialities_json(content):
    dialect = csv.Sniffer().sniff(content)
    cr = csv.reader(content.splitlines(), dialect)
    return [{"value": row[4], "category": "Municipality"} for row in cr if len(row) > 3]


def get_austrian_municipialities():
    url = "https://edm.gv.at/edm_portal/redaList.do?seqCode=8yc33c74k8xcc2&6578706f7274=1&display=plain&d-49520-e=1"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors

        json_data = response.text
        transformed_data = sorted(transform_austrian_municipialities_json(json_data), key=lambda x: x["value"])

        result_data = {
            "version": 1,
            "data": [
                {
                    "name": "Municipalities",
                    "description": f"List of Austrian Municipalities {datetime.now().isoformat()}",
                    "usage": 4,
                    "link": "https://raw.githubusercontent.com/ait-cs-IaaS/wordlists/master/output/austrian_municipalities.json",
                    "entries": transformed_data,
                }
            ],
        }

        with open("output/austrian_municipalities.json", "w") as output_file:
            json.dump(result_data, output_file, indent=4, ensure_ascii=False)

        print(f"Saved {len(transformed_data)} entries to output/austrian_municipalities.json successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # get_countries()
    get_austrian_municipialities()
