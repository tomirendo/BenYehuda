from setuptools import setup, find_packages

setup(
    name="scrapper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ]
)

