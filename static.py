import json


def transform_static_json(file_path, category):
    with open(f"data/{file_path}") as f:
        data = f.read().splitlines()
        return [{"value": name, "category": category} for name in data]


def get_static_list(static_file: str, category: str, result_file: str, name: str, description: str = ""):
    try:
        transformed_data = sorted(transform_static_json(static_file, category), key=lambda x: x["value"])

        result_data = {
            "version": 1,
            "data": [
                {
                    "name": name,
                    "description": description,
                    "usage": 4,
                    "link": f"https://raw.githubusercontent.com/ait-cs-IaaS/wordlists/master/output/{result_file}",
                    "entries": transformed_data,
                }
            ],
        }

        with open(f"output/{result_file}", "w") as output_file:
            json.dump(result_data, output_file, indent=4, ensure_ascii=False)

        print(f"Saved {len(transformed_data)} entries to output/countries.json successfully!")

    except Exception as e:
        print(f"Error: {e}")


def get_static_lists():
    get_static_list("countries.txt", "Country", "countries_german.json", "Länder", "Liste aller Länder")
    get_static_list("companies_austria.txt", "Company", "companies_austria.json", "Unternehmen", "Größten Unternehmen in Österreich")
    get_static_list(
        "international_orgs.txt",
        "NGO",
        "ngos_german.json",
        "Internationale Organisationen",
        "Wichtigsten internationalen Organisationen",
    )


if __name__ == "__main__":
    get_static_lists()
