from setuptools import setup
from setuptools import find_packages

setup(
    name='pgp',
    version='1.0.0',
    description='This is a python script for scraping prices for gems in path of exile',
    author='Velizar Arnaudov',
    author_email='vyaryw@gmail.com',
    url='https://github.com/Vyary/poe-gem-prices',
    install_requires=['requests', 'pandas', 'tqdm'],
    packages=find_packages(),
    entry_points={'console_scripts': [
        "pgp=pgp.poe_gem_prices:main"]},
)
