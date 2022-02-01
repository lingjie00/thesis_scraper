"""Extract a sample API request from Finage."""
import logging
import json
import configparser
import requests

logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read("key.ini")

# API key
_API = config["DEFAULT"]["API"]

# symbol
symbol = "ULVR.L"

# website
site = "https://api.finage.co.uk/income-statement/"

# period (quarter or annual)
period = "quarter"

# link
link = site + symbol + "?&period=" + period + "&apikey=" + _API

logging.info(f"Request link {link}")

response = requests.get(link)

content = response.json()

logging.info(content)

with open(f"output/{symbol}.json", "w") as file:
    out = json.dumps(content)
    file.write(out)
