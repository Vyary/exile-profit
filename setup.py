from setuptools import setup
from setuptools import find_packages

setup(
    name='poe-gem-prices',
    version='1.0.1',
    description='Path of exile gem price scraper',
    author='Velizar Arnaudov',
    author_email='vyaryw@gmail.com',
    url='https://github.com/Vyary/poe-gem-prices',
    install_requires=['requests', 'pandas'],
    packages=find_packages(),
    entry_points={'console_scripts': [
        "poe-gem-prices=src.core:main"]},
)
