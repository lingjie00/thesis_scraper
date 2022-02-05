"""Extract a sample API request from Finage."""
import logging
import json
import csv
import configparser
import requests


class Price:

    # website
    site = "https://api.finage.co.uk/agg/stock/global/uk/"

    # time
    time = "1month"  # monthly data
    start = "1991-01-01"
    to = "2022-02-01"

    def __init__(self, API, filepath):
        self.API = API
        self.filepath = filepath

    def extract(self, symbol):
        try:
            # link
            link = self.site + symbol +\
                "/" + self.time + "/" +\
                self.start + "/" + self.to +\
                "?apikey=" + self.API + "&limit=5000"

            logging.debug(f"Request link {link}")

            response = requests.get(link)

            content = response.json()

            logging.debug(content)

            if "error" in content:
                raise NotImplementedError(f"{symbol} not found: {content}")

            with open(f"{self.filepath}/{symbol}_price.json", "w") as file:
                out = json.dumps(content)
                file.write(out)

            logging.info(f"{symbol} price extracted")

        except Exception as e:
            logging.info(f"{symbol} failed to extract with")
            logging.info(e)

        finally:
            return self


def main():
    """Run price extract"""
    logging.basicConfig(filename="price.log", level=logging.INFO)

    config = configparser.ConfigParser()
    config.read("data/key.ini")

    # API key
    _API_KEY = config["DEFAULT"]["API"]

    extractor = Price(API=_API_KEY, filepath="output/price")

    with open("data/LSE_symbols.csv", "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            # symbol stored in first column
            symbol = row[0]
            logging.debug(symbol)
            extractor.extract(symbol=symbol)


if __name__ == "__main__":
    # run extraction
    main()
