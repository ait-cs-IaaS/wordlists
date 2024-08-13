import os
import re
import json
import zipfile
import requests
from datetime import datetime
from common import make_unique, get_first_names

first_names = get_first_names()


def shortest_substrings(strings: list[str]) -> list[str]:
    if not strings:
        return []

    min_str = min(strings, key=len)
    shortest_substrings = []

    for i in range(len(min_str)):
        for j in range(i + 1, len(min_str) + 1):
            substr = min_str[i:j]
            if all(substr in string for string in strings):
                shortest_substrings.append(substr)

    return (
        sorted(shortest_substrings, key=len, reverse=True)[:1]
        if shortest_substrings
        else []
    )


def not_in_blacklist(value: str) -> bool:
    if not value:
        return False
    if len(value) < 3 or len(value) > 32:
        return False
    if not value[0].isalpha() or value[0].islower():
        return False
    if value in {
        "subsidiary",
        "division",
        "subsidiaries",
        "divisions",
        "CI Server",
        "DHCP",
        "Name Directory",
        "Money Forward for",
        "Adaptive Delivery",
        "Modicon Quantum ",
        "Billing Software",
        "Typing Text",
        "Two Factor",
        "Firewall",
        "Firewall Module",
        "Japan",
    }:
        return False
    if any(
        check_str in value.lower()
        for check_str in {
            "admin",
            "azure ",
            "add ",
            "bmc ",
            "advanced",
            "assistant",
            "before",
            "coming soon",
            "cam ",
            "campaign",
            "charx ",
            "cics ",
            "contact ",
            "cookie ",
            "codesys ",
            "custom ",
            "copy ",
            "create ",
            "c-more ",
            "ccx ",
            "dr-",
            "dsl-",
            "e-commerce",
            "er ",
            "email",
            "event",
            "ex ",
            "edge ",
            "futurenet ",
            "gallery",
            "gift ",
            "global ",
            "gv_",
            "itk-",
            "image ",
            "logiq ",
            "lnl-",
            "logo!",
            "none",
            "unknown",
            "n/a",
            "version",
            "scalance",
            "simantic",
            "migration",
            "migrate",
            "melsec",
            "mobile",
            "modicon",
            "open ",
            "page ",
            "post ",
            "portal ",
            "product ",
            "ruggedcom ",
            "redirection",
            "remote ",
            "responsive ",
            "simatic ",
            "siplus ",
            "siprotec ",
            "template",
            "quotes ",
            "quiz ",
            "vvx ",
            "video ",
            "/",
            "|",
        }
    ):
        return False
    if all(not char.isalpha() for char in value):
        return False
    if any(re.match(f"^{name}\s\w+$", value) for name in first_names):
        return False
    return True


def cleanup_value(input_str: str) -> str:
    cleaned_str = re.sub(r"\([^)]*\)", "", input_str)
    cleaned_str = re.sub(r"\[[^\]]*\]", "", cleaned_str)
    cleaned_str = re.sub(r"\{[^\}]*\}", "", cleaned_str)
    cleaned_str = re.sub(r"[\(\)\[\]\{\}]", "", cleaned_str)
    cleaned_str = re.sub(r"^[A-Z]{1,3}\d*$", "", cleaned_str)
    cleaned_str = re.sub(r"\s+", " ", cleaned_str)
    return cleaned_str.strip()
    # return "".join(char for char in input_str if char.isalnum() or char.isspace()).strip()


def get_affected(json_data, category) -> set[str]:
    affected_entries = set()
    for entry in json_data.get("containers", {}).get("cna", {}).get("affected", []):
        if value := entry.get(category):
            for value in re.split(r",|AND|and", value):
                value = cleanup_value(value)
                if not_in_blacklist(value):
                    affected_entries.add(value)
    return affected_entries


def create_data(original_json, category):
    affected_entries = get_affected(original_json, category)
    cve_id = original_json.get("cveMetadata", {}).get("cveId", "")

    # affected_entries = shortest_substrings(list(affected_entries))

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
        print(
            "Please download the CVE JSON files from https://github.com/CVEProject/cvelistV5/releases"
        )
        print(
            "and extract them to /tmp/cve/ with `unzip -j cvelistv5.zip -d /tmp/cve/`"
        )
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

    json_files = [
        cve_file
        for cve_file in os.listdir(rootdir)
        if cve_file.endswith(".json") and cve_file.startswith("CVE-")
    ]

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

    print(
        f"Saved {len(vendor_data['data'][0]['entries'])} entries to output/vendors.json successfully!"
    )

    # Write the result to products.json
    with open("output/products.json", "w") as output_file:
        json.dump(product_data, output_file, indent=4, ensure_ascii=False)

    print(
        f"Saved {len(product_data['data'][0]['entries'])} entries to output/products.json successfully!"
    )


def get_latest_release_download_url(endswith_str):
    api_url = "https://api.github.com/repos/CVEProject/cvelistV5/releases/latest"

    response = requests.get(api_url)
    response.raise_for_status()
    release_data = response.json()

    download_url = next(
        (
            asset["browser_download_url"]
            for asset in release_data["assets"]
            if asset["name"].endswith(endswith_str)
        ),
        None,
    )
    download_file(download_url, "/tmp/cve/cvelistv5.zip")
    unzip_flatten("/tmp/cve/cvelistv5.zip", "/tmp/cve/")


def unzip_flatten(zip_path, output_dir):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for zip_info in zip_ref.infolist():
            zip_info.filename = os.path.basename(zip_info.filename)

            if zip_info.filename:
                zip_ref.extract(zip_info, output_dir)


def download_file(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))
    downloaded_size = 0

    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            downloaded_size += len(chunk)
            f.write(chunk)

            progress_percentage = (downloaded_size / total_size) * 100
            print(f"\rDownloading... {progress_percentage:.2f}% complete", end="")
    print("\nDownload finished.")


if __name__ == "__main__":
    # get_latest_release_download_url("midnight.zip.zip")
    get_cves()
