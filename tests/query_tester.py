import json

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Content-Type": "application/json",
}

query = {
    "query": {
        "status": {"option": "online"},
        "type": "Absolution",
        "stats": [{"type": "and", "filters": []}],
        "filters": {
            "misc_filters": {
                "filters": {
                    "quality": {"min": 20},
                    "gem_level": {"min": 20},
                    "gem_alternate_quality": {"option": 0},
                    "corrupted": {"option": "true"},
                }
            },
            "trade_filters": {
                "filters": {
                    "collapse": {"option": "true"},
                    "indexed": {"option": "3days"},
                }
            },
        },
    },
    "sort": {"price": "asc"},
}

trade_url: str = "https://www.pathofexile.com/api/trade/search/Standard"
payload = json.dumps(query)

get_results_ids = requests.request("POST", trade_url, headers=headers, data=payload)

print(get_results_ids.headers["X-Rate-Limit-Ip"])
print(get_results_ids.headers["X-Rate-Limit-Ip-State"])

total_listed = json.loads(get_results_ids.text)["total"]
search_id = json.loads(get_results_ids.text)["id"]

if total_listed < 12:
    results_list = json.loads(get_results_ids.text)["result"][:10]
else:
    results_list = json.loads(get_results_ids.text)["result"][2:12]

items_link = (
    f"https://www.pathofexile.com/api/trade/fetch/"
    f"{','.join(results_list)}?query={search_id}"
)
api_response = requests.request("GET", items_link, headers=headers)

item_data = json.loads(api_response.text)["result"]

for item in item_data:
    amount = item["listing"]["price"]["amount"]
    type_of_currency = item["listing"]["price"]["currency"]
    print(f"{amount} x {type_of_currency}")
