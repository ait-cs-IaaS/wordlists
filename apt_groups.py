import requests
import csv
import json

from common import filter_stopword

BASE_URL = "https://docs.google.com/spreadsheets/d/1H9_xaxQHpWaa4O_Son4Gx0YOIzlcBWMsdvePFX68EKU/export?format=csv&gid="

gids = [361554658, 1636225066, 1905351590, 376438690, 300065512, 2069598202, 574287636, 438782970]


def extract_apt_groups() -> dict:
    all_data = {}

    for gid in gids:
        try:
            response = requests.get(BASE_URL + str(gid))
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch data for gid {gid}. Error: {e}")
            continue

        lines = response.content.decode("utf-8").splitlines()

        # Extract the country name from the first line
        country = lines[0].split(",")[0]

        # Set headers for DictReader
        headers = lines[1].split(",")

        csv_data = lines[2:]  # Data starting from the third line

        reader = csv.DictReader(csv_data, fieldnames=headers)
        country_data = []

        # Extract "Common Name" and "CrowdStrike" columns
        for row in reader:
            common_name = row.get("Common Name", None)
            crowdstrike = row.get("CrowdStrike", None)

            if common_name:
                country_data.append(common_name)
            if crowdstrike:
                country_data.append(crowdstrike)

        all_data[country] = sorted(list(set(country_data)))  # Deduplication per country

    return all_data


def get_apt():
    apt_groups_by_country = extract_apt_groups()

    entries = []
    for country, groups in apt_groups_by_country.items():
        for group in groups:
            if filter_stopword(group):
                continue
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
