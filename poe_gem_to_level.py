import requests
import pandas as pd
from tqdm import tqdm
import gem_class


def gem_quality_type(name):
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


def create_gem_object(gem_name, variant, price, quality, listed, lst, new_gem):
    if any(obj.name == gem_name for obj in lst) is False and quality != 'Awakened':
        lst.append(new_gem)
    return any(change_price(obj, variant, price, quality, listed) for obj in lst if obj.name == gem_name)


def change_price(gem, variant, price, quality, listed):
    if variant == "1/20" and quality == 'Basic' or variant == "1" and quality == 'Alternative':
        gem.base_price = price
    elif variant == "20/20c" and quality != 'Vaal':
        gem.fail_price = price
    elif variant == "20/20c" and quality == 'Vaal':
        gem.vaal_price = price
    elif variant == "21/20c" and quality != 'Vaal':
        gem.success_price = price
        gem.listed = listed


def go_over_elements(data):
    for index, gem_full in enumerate(tqdm(data["lines"])):
        gem_name = data["lines"][index]['name']
        variant = data["lines"][index]['variant']
        price = data["lines"][index]['chaosValue']
        listed = data["lines"][index]['listingCount']

        quality = gem_quality_type(gem_name)
        if quality == 'Vaal':
            gem_name = gem_name.split('Vaal ')
            gem_name = ''.join(gem_name)

        new_gem = gem_class.Gem(gem_name)
        lst = gem_class.Gem.gem_lst

        create_gem_object(gem_name, variant, price, quality, listed, lst, new_gem)


def save_data():
    save_lst = [[x.name, x.base_price, x.fail_price, x.success_price, x.vaal_price, x.listed]
                for x in gem_class.Gem.gem_lst]
    df = pd.DataFrame(save_lst)
    df = df.set_axis(['Gem Name', 'Base', '20/20', '21/20', 'Vaal price', 'Listed'], axis=1)
    df.to_csv('gems.csv', index=False, encoding='utf-8')


def main():
    url = "https://poe.ninja/api/data/itemoverview?league=Kalandra&type=SkillGem&language=en"
    response = requests.get(url).json()
    go_over_elements(response)
    save_data()


if __name__ == '__main__':
    main()
