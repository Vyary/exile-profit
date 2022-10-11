price_value = '5.3k'

check = {
    '0k': '000',
    '1k': '100',
    '2k': '200',
    '3k': '300',
    '4k': '400',
    '5k': '500',
    '6k': '600',
    '7k': '700',
    '8k': '800',
    '9k': '900',
}

try:
    price_value = price_value.split('.')[0] + check[price_value.split('.')[1]]
except IndexError:
    pass

print(price_value)
