from typing import List
import requests
import pandas as pd
import gems


def gem_quality_type(name: str) -> str:
    """
    Gets a gem's quality type based on its prefix.
    :param name: The gem's name.
    :return: The gem's quality type.
    """
    # Split the gem name into parts
    gem_name_parts = name.split(" ")

    # Create a dictionary of gem quality types and their corresponding prefixes
    quality_types: dict[str, List[str]] = {
        "Vaal": ["Vaal"],
        "Alternative": ["Anomalous", "Divergent", "Phantasmal"],
        "Awakened": ["Awakened"],
    }

    # Loop through the dictionary and check if the gem name
    # has a prefix that matches any of the quality types
    for quality, prefixes in quality_types.items():
        for prefix in prefixes:
            if prefix in gem_name_parts:
                return quality

    # If no prefix was found, return "Basic"
    return "Basic"


def create_gem_object(
    gem_name: str, variant: str, price: float, quality: str, listed: int
) -> None:
    """
    Creates gem object in the gem class if it doesn't exist and
    updates the given prices
    :param gem_name: Gem's name
    :param variant: Gem variants can be 1, 1-20, 20/20c, 21/20c
    :param price: Price of the gem of current variant
    :param quality: Quality type
    :param listed: Number of listings for the successful gems of set gem
    :return: None
    """
    # Get the list of gem objects
    lst = gems.Gem.lst

    # Check if there is object with the set name if not create new object
    if any(obj.name == gem_name for obj in lst) is False:
        new_object = gems.Gem(gem_name)
        lst.append(new_object)

    # Update the attributes of the matching gem object
    for obj in lst:
        if obj.name == gem_name:
            if (
                variant == "1/20"
                and quality == "Basic"
                or variant == "1"
                and quality == "Alternative"
            ):
                obj.base_price = price
            elif variant == "20/20c" and quality != "Vaal":
                obj.fail_price = price
            elif variant == "20/20c" and quality == "Vaal":
                obj.vaal_price = price
            elif variant == "21/20c" and quality != "Vaal":
                obj.success_price = price
                obj.listed = listed


def go_over_elements(data: dict) -> list:
    """
    Core function that goes over the collected data from the api and
    calls a function to create object for each gem
    :param data: Collected data from the api
    :return: List of objects
    """
    # Loop over the gems in the data(api response)
    for gem in data["lines"]:
        gem_name = gem["name"]
        variant = gem["variant"]
        price = gem["chaosValue"]
        listed = gem["listingCount"]

        # Get the gem's quality
        quality = gem_quality_type(gem_name)

        # Handle special cases for gems with the "Vaal" or "Awakened" quality
        if quality == "Vaal":
            gem_name = gem_name.split("Vaal ")
            gem_name = "".join(gem_name)
        elif quality == "Awakened":
            continue

        # Create a gem object for the current gem
        create_gem_object(gem_name, variant, price, quality, listed)

    # Return the list of gem objects
    return gems.Gem.lst


def save_data(list_of_objects: list) -> None:
    """
    Function to go over all objects in the class list, make a dataframe and
    save the information in csv file in descending order by success price
    :param list_of_objects: Gem class list
    :return: None
    """
    save_lst = [
        [
            x.name,
            x.base_price,
            x.fail_price,
            x.success_price,
            x.vaal_price,
            x.listed,
        ]
        for x in list_of_objects
    ]

    # Sort the gem data by success price in descending order
    sorted_save_lst = sorted(save_lst, key=lambda x: x[3], reverse=True)

    # Create a DataFrame from the sorted gem data
    df = pd.DataFrame(
        sorted_save_lst,
        columns=["Gem Name", "Base", "20/20", "21/20", "Vaal price", "Listed"],
    )

    # Save the DataFrame as a CSV file
    df.to_csv("output/gems.csv", index=False, encoding="utf-8")


def main():
    # Set the URL for the API call
    url = (
        "https://poe.ninja/api/data/itemoverview?league="
        "Kalandra&type=SkillGem&language=en"
    )
    # Send a request to the API and get the response
    response = requests.get(url).json()
    # Get a list of gem objects from the response
    list_of_objects = go_over_elements(response)
    # Save the gem data to a CSV file
    save_data(list_of_objects)


if __name__ == "__main__":
    main()
