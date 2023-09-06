import os
import json
from datetime import datetime
from common import make_unique


def get_affected(json_data, category):
    affected_entries = set()
    for entry in json_data.get("containers", {}).get("cna", {}).get("affected", []):
        if value := entry.get(category):
            if "," in value:
                for value in value.split(","):
                    affected_entries.add(value)
            else:
                affected_entries.add(value)
    return affected_entries


def create_data(original_json, category):
    affected_entries = get_affected(original_json, category)
    cve_id = original_json.get("cveMetadata", {}).get("cveId", "")

    return [
        {
            "value": entry.strip(),
            "category": f"CVE_{category.upper()}",
            "description": f"{cve_id}",
        }
        for entry in affected_entries
    ]


def get_cves():
    rootdir = "/tmp/cve/"

    if not os.path.exists(rootdir):
        print(f"Error: {rootdir} does not exist")
        print("Please download the CVE JSON files from https://github.com/CVEProject/cvelistV5/releases")
        print("and extract them to /tmp/cve/ with `unzip -j cvelistv5.zip -d /tmp/cve/`")
        return

    vendor_data = {
        "version": 1,
        "data": [
            {
                "name": "CVE_VENDORS",
                "description": f"Vendors Exported from CVEList {datetime.now().isoformat()}",
                "usage": 4,
                "link": "https://raw.githubusercontent.com/ait-cs-IaaS/wordlists/master/output/vendors.json",
                "entries": [],
            }
        ],
    }
    product_data = {
        "version": 1,
        "data": [
            {
                "name": "CVE_PRODUCTS",
                "description": f"Products Exported from CVEList {datetime.now().isoformat()}",
                "usage": 4,
                "link": "https://raw.githubusercontent.com/ait-cs-IaaS/wordlists/master/output/products.json",
                "entries": [],
            }
        ],
    }

    json_files = [cve_file for cve_file in os.listdir(rootdir) if cve_file.endswith(".json") and cve_file.startswith("CVE-")]

    for file_name in json_files:
        with open(os.path.join(rootdir, file_name), "r") as json_file:
            original_json = json.load(json_file)
            vendor_data_list = create_data(original_json, "vendor")
            product_data_list = create_data(original_json, "product")

            vendor_data["data"][0]["entries"].extend(vendor_data_list)
            product_data["data"][0]["entries"].extend(product_data_list)

    vendor_data["data"][0]["entries"] = make_unique(vendor_data["data"][0]["entries"])
    product_data["data"][0]["entries"] = make_unique(product_data["data"][0]["entries"])

    # Write the result to vendors.json
    with open("output/vendors.json", "w") as output_file:
        json.dump(vendor_data, output_file, indent=4, ensure_ascii=False)

    print(f"Saved {len(vendor_data['data'][0]['entries'])} entries to output/vendors.json successfully!")

    # Write the result to products.json
    with open("output/products.json", "w") as output_file:
        json.dump(product_data, output_file, indent=4, ensure_ascii=False)

    print(f"Saved {len(product_data['data'][0]['entries'])} entries to output/products.json successfully!")


if __name__ == "__main__":
    get_cves()
