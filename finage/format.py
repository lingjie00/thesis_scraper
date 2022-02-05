import pandas as pd
import json
import logging

logging.basicConfig(level=logging.INFO)

fundamental = pd.read_json("output/ULVR.L.json")

logging.info(fundamental)

fundamental.to_csv("output/unilever_fundamental.csv", index=False)

with open("output/ULVR_price.json", "r") as file:
    loaded = json.loads(file.read())
    price = pd.json_normalize(loaded["results"])
    price["symbol"] = "ULVR"

logging.info(price)

price.to_csv("output/unilever_price.csv", index=False)
