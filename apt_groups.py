import requests
import csv
import json

BASE_URL = "https://docs.google.com/spreadsheets/d/1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU/export?format=csv&gid=856560690"


def extract_apt_groups() -> dict:
    all_data = {}

    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch data for gid {BASE_URL}. Error: {e}")

    lines = response.content.decode("utf-8").splitlines()

    # Set headers for DictReader
    headers = lines[2].split(",")

    csv_data = lines[3:]  # Data starting from the fourth line

    reader = csv.DictReader(csv_data, fieldnames=headers)

    # Extract "Common Name" and "Country" columns
    for row in reader:
        common_name = row.get("New name", None)
        country = row.get("Origin/Threat", None)
        if not common_name or not country:
            continue
        if country not in all_data:
            all_data[country] = []
        all_data[country].append(common_name)

    return all_data


def get_apt():
    apt_groups_by_country = extract_apt_groups()

    entries = []
    for country in apt_groups_by_country:
        for group in apt_groups_by_country[country]:
            entry = {"value": group, "category": "APT", "description": f"{country} APT"}
            entries.append(entry)

    result_data = {
        "version": 1,
        "data": [
            {
                "name": "APT",
                "description": "List of APT groups",
                "usage": 4,
                "link": "https://raw.githubusercontent.com/ait-cs-IaaS/wordlists/master/output/apt.json",
                "entries": entries,
            }
        ],
    }

    with open("output/apt.json", "w") as output_file:
        json.dump(result_data, output_file, indent=4, ensure_ascii=False)

    print(f"Saved {len(entries)} entries to output/apt.json successfully!")


if __name__ == "__main__":
    get_apt()
