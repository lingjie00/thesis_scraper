import pandas as pd
import json
import logging

logging.basicConfig(level=logging.INFO)

annual = pd.read_json("unilever_annual.json")

logging.info(annual)

annual.to_csv("unilever_annual.csv", index=False)

quarter = pd.read_json("unilever_quarter.json")

logging.info(quarter)

quarter.to_csv("unilever_quarter.csv", index=False)

with open("unilever_price.json", "r") as file:
    loaded = json.loads(file.read())
    price = pd.json_normalize(loaded["results"])

logging.info(price)

price.to_csv("unilever_price.csv", index=False)
