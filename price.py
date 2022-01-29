"""Extract a sample API request from Finage."""
import logging
import json
import requests

logging.basicConfig(level=logging.INFO)

# API key
_API_KEY = "API_KEY14IDEPF7SA61VQ8243EN1FOJTLXQT4T0"

# symbol
symbol = "ULVR"

# website
site = "https://api.finage.co.uk/agg/stock/global/uk/"

# time
time = "1month"  # monthly data
start = "1991-01-01"
to = "2021-12-01"

# link
link = site + symbol + "/" + time + "/" + start + "/" + to +\
    "?apikey=" + _API_KEY + "&limit=5000"

logging.info(f"Request link {link}")

response = requests.get(link)

content = response.json()

logging.info(content)

with open(f"{symbol}_price.json", "w") as file:
    out = json.dumps(content)
    file.write(out)
