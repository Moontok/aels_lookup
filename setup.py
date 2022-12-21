from setuptools import setup

setup(
    name='aels_license_validator',
    version="1.0",
    packages=["aels_license_validator"],
    install_requires=[
        "playwright",
        "bs4"
    ]
)