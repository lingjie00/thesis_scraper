"""Extract a sample API request from Finage."""
import logging
import json
import requests

logging.basicConfig(level=logging.INFO)

# API key
_API = "API_KEY11X3NFOGGAN3NGXWKXHP58NBWQ7IPFKB"

# firm
firm = "ULVR.L"

# website
site = "https://api.finage.co.uk/income-statement/"

# period
period = "quarter"

# link
link = site + firm + "?&period=" + period + "&apikey=" + _API

logging.info(f"Request link {link}")

response = requests.get(link)

content = response.json()

logging.info(content)

with open(f"{firm}.json", "w") as file:
    out = json.dumps(content)
    file.write(out)
