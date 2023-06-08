import csv
from typing import Any, Dict, List


class SaveData:
    def save_list_to_csv(self, file_name: str, item_data: List[Any]):
        items_list: List[Dict[str, str]] = [item.__dict__ for item in item_data]

        new_data: List[Dict[str, str]] = []

        for row in items_list:
            new_row = {}

            for key, value in row.items():
                split_key = key.split("_")
                capitalized_key = " ".join(word.capitalize() for word in split_key)
                new_row[capitalized_key] = value

            new_data.append(new_row)

        keys = new_data[0].keys()

        with open(f"output/{file_name}", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(new_data)

    def save_dict_to_csv(
        self, file_name: str, data_dictionary: Dict[str, Any], sort_by: str = None
    ):
        if not isinstance(next(iter(data_dictionary.values())), type({})):
            data_dictionary = {
                name: data.__dict__ for name, data in data_dictionary.items()
            }

        if sort_by:
            sorted_data = sorted(
                data_dictionary.items(), key=lambda x: x[1][sort_by], reverse=True
            )
        else:
            sorted_data = data_dictionary.items()

        new_dict_with_capitalized_keys: Dict[str, Dict[str, str]] = {}

        for name, dict in sorted_data:
            new_dict_with_capitalized_keys[name] = {}
            for key, value in dict.items():
                split_key = key.split("_")
                capitalized_key = " ".join(word.capitalize() for word in split_key)
                new_dict_with_capitalized_keys[name][capitalized_key] = value

        fieldnames = list(new_dict_with_capitalized_keys.values())[0].keys()

        with open(f"output/{file_name}", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(new_dict_with_capitalized_keys.values())
