from setuptools import setup, find_packages

setup(
    name="ip_lookup_tool",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "requests",
        "openpyxl",
        "typer[all]",
    ],
    entry_points={
        "console_scripts": [
          "ip-lookup = src.ip_lookup:main_entry",  
        ]
    },
    author="Mikel U.",
    description="CLI tool to geolocate IP addresses and export results to Excel and KML.",
    license="MIT",
)
