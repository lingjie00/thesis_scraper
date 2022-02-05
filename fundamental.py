"""Extract fundamental data from Finage."""
import logging
import json
import csv
import configparser
import requests


class Fundamental:
    # website
    site = "https://api.finage.co.uk/income-statement/"

    def __init__(self, API, filepath, period="quarter"):
        self.API = API
        self.filepath = filepath
        # period (quarter or annual)
        self.period = period

    def extract(self, symbol):
        try:
            # link
            link = self.site + symbol + ".L" +\
                "?&period=" + self.period +\
                "&apikey=" + self.API
            logging.debug(f"Request link {link}")
            response = requests.get(link)

            content = response.json()
            logging.debug(content)

            if "error" in content:
                raise NotImplementedError(f"{symbol} not found: {content}")

            with open(f"{self.filepath}/{symbol}.json", "w") as file:
                out = json.dumps(content)
                file.write(out)

            logging.info(f"{symbol} fundamental data extracted")

        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise KeyboardInterrupt()
            logging.info(f"{symbol} failed to extract with")
            logging.info(e)

        finally:
            return self


def main():
    """Run extraction."""
    logging.basicConfig(filename="fundamental.log", level=logging.INFO)

    config = configparser.ConfigParser()
    config.read("data/key.ini")

    # API key
    _API = config["DEFAULT"]["API"]

    # filepath
    filepath = "output/fundamental"

    extractor = Fundamental(_API, filepath)

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
