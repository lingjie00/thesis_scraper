# %%
"""Runs the scraper."""
import configparser
import csv
import logging

from finage import Fundamental, Price

# notebook has a different working dir from project
relative_path = "../"


def extract():
    """Run extraction."""
    logging.basicConfig(
        filename=relative_path+"test.log",
        level=logging.INFO)

    config = configparser.ConfigParser()
    config.read(relative_path + "data/key.ini")

    logging.debug(config["DEFAULT"])

    # API key
    _API = config["DEFAULT"]["API"]

    # files
    fundamental_filepath = relative_path+"output/fundamental"
    price_filepath = relative_path+"output/price"
    fundamental_filepath = relative_path+"output/test_output"
    price_filepath = relative_path+"output/test_output"
    symbol_file = relative_path+"data/LSE_symbols.csv"
    symbol_file = relative_path+"data/symbol_test.csv"

    fundamental_extractor = Fundamental(_API, fundamental_filepath)

    with open(symbol_file, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            # symbol stored in first column
            symbol = row[0]
            logging.debug(symbol)
            fundamental_extractor.extract(symbol=symbol)

    price_extractor = Price(API=_API, filepath=price_filepath)

    with open(symbol_file, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            # symbol stored in first column
            symbol = row[0]
            logging.debug(symbol)
            price_extractor.extract(symbol=symbol)


extract()
