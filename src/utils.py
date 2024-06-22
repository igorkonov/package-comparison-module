import json


def get_dump_json(data: list[dict]) -> json:
    with open('packages.json', 'w', encoding='utf-8') as f:
        return json.dump(data, f, indent=2, ensure_ascii=False)
