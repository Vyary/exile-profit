import requests
import pandas as pd
from tqdm import tqdm
import gem_class


def gem_quality_type(name: str) -> str:
    """
    Checks gem's prefix and returns quality type
    :param name: Gem's name
    :return: Quality type of the gem
    """
    split_name = name.split(' ')
    if len(split_name) > 1:
        if split_name[0] == 'Vaal' or split_name[1] == 'Vaal':
            return 'Vaal'
    if split_name[0] == 'Anomalous' or split_name[0] == 'Divergent' or split_name[0] == 'Phantasmal':
        return 'Alternative'
    if split_name[0] == 'Awakened':
        return 'Awakened'
    else:
        return 'Basic'


def create_gem_object(gem_name: str, variant: str, price: float, quality: str, listed: int, lst: list) -> None:
    """
    Creates gem object in the gem class if it doesn't exist and updates given prices if it does
    :param gem_name: Gem's name
    :param variant: Gem variants can be 1, 1-20, 20/20c, 21/20c
    :param price: Price of the gem of current varint
    :param quality: Quality type
    :param listed: How many successful set gem are listed on the market including offline listings
    :param lst: List of gem objects in gem class
    :return: None
    """
    # Check if there is object with the set name if not create new object
    if any(obj.name == gem_name for obj in lst) is False:
        new_object = gem_class.Gem(gem_name)
        lst.append(new_object)
    # Call a function to change the price
    for obj in lst:
        if obj.name == gem_name:
            if variant == "1/20" and quality == 'Basic' or variant == "1" and quality == 'Alternative':
                obj.base_price = price
            elif variant == "20/20c" and quality != 'Vaal':
                obj.fail_price = price
            elif variant == "20/20c" and quality == 'Vaal':
                obj.vaal_price = price
            elif variant == "21/20c" and quality != 'Vaal':
                obj.success_price = price
                obj.listed = listed


def go_over_elements(data: dict) -> list:
    """
    Core function going over the collected data from the api and calls the function to create the object
    :param data: Collected date from the api
    :return: List of objects
    """
    for index in tqdm(range(len(data["lines"]))):
        gem_name = data["lines"][index]['name']
        variant = data["lines"][index]['variant']
        price = data["lines"][index]['chaosValue']
        listed = data["lines"][index]['listingCount']

        quality = gem_quality_type(gem_name)
        if quality == 'Vaal':
            gem_name = gem_name.split('Vaal ')
            gem_name = ''.join(gem_name)
        elif quality == 'Awakened':
            continue

        lst = gem_class.Gem.gem_lst
        create_gem_object(gem_name, variant, price, quality, listed, lst)
    return gem_class.Gem.gem_lst


def save_data(list_of_objects: list) -> None:
    """
    Function to go over all objects in the class list, make a dataframe and
    save the information in csv file in descending order by success price
    :param list_of_objects: Gem class list
    :return: None
    """
    save_lst = [[x.name, x.base_price, x.fail_price, x.success_price, x.vaal_price, x.listed]
                for x in list_of_objects]
    save_lst = sorted(save_lst, key=lambda x: x[3], reverse=True)
    df = pd.DataFrame(save_lst)
    df = df.set_axis(['Gem Name', 'Base', '20/20', '21/20', 'Vaal price', 'Listed'], axis=1)
    df.to_csv('gems.csv', index=False, encoding='utf-8')


def main():
    url = "https://poe.ninja/api/data/itemoverview?league=Kalandra&type=SkillGem&language=en"
    response = requests.get(url).json()
    list_of_objects = go_over_elements(response)
    save_data(list_of_objects)


if __name__ == '__main__':
    main()
