from setuptools import setup, find_packages

setup(
    name='aels_license_validator',
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "playwright",
        "bs4"
    ]
)