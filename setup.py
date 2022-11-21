from setuptools import setup
from setuptools import find_packages

setup(
    name='poe-gem-prices',
    version='1.0.0',
    description='This is a python script for scraping prices for gems in path of exile',
    author='Velizar Arnaudov',
    author_email='vyaryw@gmail.com',
    url='https://github.com/Vyary/poe-gem-prices',
    install_requires=['requests', 'pandas', 'tqdm'],
    packages=find_packages(),
    entry_points={'console_scripts': [
        "poe-gem-prices=poe_gem_prices.core:main"]},
)
