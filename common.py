from stopwords import stop_words
import json


def make_unique(data_list):
    unique_entries = set()
    result_list = []
    for data in sorted(data_list, key=lambda x: x["value"]):
        value = data["value"].lower()
        if filter_stopword(value) or (not value.islower()):
            continue
        if value not in unique_entries:
            unique_entries.add(value)
            result_list.append(data)

    return result_list


def filter_stopword(value):
    return value in stop_words or len(value) < 3


common_words = [
    "Gh0st RAT",
    "Poison Ivy",
    "HydraQ",
    "Hikit",
    "Zxshell",
    "DeputyDog",
    "PlugX",
    "BACKSPACe",
    "HttpBrowser",
    "NetTraveler",
    "IceFog",
    "HTran",
    "Agent.BTZ",
    "Comfoo",
    "DNSChanger",
    "IEXPLORE RAT",
    "LStudio",
    "MNKit",
    "Derusbi",
    "Wipbot",
    "Carbon Rootkit",
    "Turla",
    "Mimikatz",
    "HDRoot",
    "OrcaRAT",
    "Etumbot",
    "NjRAT",
    "X-Agent",
    "Adwind RAT",
    "Jiripbot",
    "Quasar RAT",
    "FallChill",
    "DustySky",
    "Exforel",
    "LoJax",
    "ROKRAT",
    "Xtunnel",
    "Zebrocy",
    "SeduUploader",
    "Sofacy",
    "BlackEnergy",
    "BlackEnergy2 ",
    "GreyEnergy Mini",
    "Industroyer",
    "NotPetya",
    "Data breach",
    "Security breach",
    "Malware attack",
    "Password reset",
    "Phishing email",
    "Vulnerability assessment",
    "Network intrusion",
    "Firewall rule",
    "Cybersecurity incident",
    "Incident response",
    "(APT)",
    "Advanced persistent threat",
    "Zero-day vulnerability exploit",
    "Security incident report",
    "Social engineering attack",
    "(MFA)",
    "Multi-factor authentication",
    "Denial of service",
    "Data exfiltration attempt",
    "Security policy violation",
    "Intrusion detection system",
    "Security awareness training",
    "SIEM",
    "zero-day",
    "ransomware",
    "phishing",
    "man-in-the-middle",
    "keylogger",
    "blockchain",
    "supply chain",
    "SQL-Injections",
    "SQL Injection",
]


def get_first_names():
    with open("data/names.txt", "r") as f:
        return f.read().splitlines()


def get_common_words():
    entries = [{"value": word, "category": "Cybersecurity"} for word in sorted(common_words)]
    result_data = {
        "version": 1,
        "data": [
            {
                "name": "Common IT Security Terms",
                "description": "List of common IT security terms",
                "usage": 4,
                "link": "https://raw.githubusercontent.com/ait-cs-IaaS/wordlists/master/output/common.json",
                "entries": entries,
            }
        ],
    }

    with open("output/common.json", "w") as output_file:
        json.dump(result_data, output_file, indent=4, ensure_ascii=False)

        print(f"Saved {len(entries)} entries to output/common.json successfully!")


if __name__ == "__main__":
    get_common_words()
