"""Runs the extractor."""
import configparser
import csv
import logging

from fundamental import Fundamental
from price import Price


def extract(
        symbol_file: str,
        fundamental_filepath: str,
        price_filepath: str,
        output_format: str,
        api_file: str,
        time: str,
        period: str,
        run_price: bool = True,
        run_fundamental: bool = True
):
    """Run extraction.

    params:
        symbol_file: file that stores the list of symbols
        fundamental_filepath: path to save the fundamental data
        price_filepath: path to save the price data
        output_format: choose either csv or json
        api_file: path to load the API key (in .ini format)
        time: frequency of extraction for price data
        period: frequency of extraction for fundamental data
        run_price: do we extract price data
        run_fundamental: do we extract fundamental data
    """
    # we use configparser to load API keys
    config = configparser.ConfigParser()
    config.read(api_file)

    logging.debug(config["DEFAULT"])

    # API key
    _API = config["DEFAULT"]["API"]

    # Initiate the extractors
    fundamental_extractor = Fundamental(
        api=_API, filepath=fundamental_filepath, period=period)
    price_extractor = Price(
        api=_API, filepath=price_filepath, time=time)

    symbol = "INIT"

    try:
        # for extractor in (fundamental_extractor, price_extractor):
        for extractor in (price_extractor, fundamental_extractor):
            if not run_price and isinstance(extractor, Price):
                continue
            if not run_fundamental and isinstance(extractor, Fundamental):
                continue
            logging.debug(f"Running {type(extractor)}")
            if output_format == "csv":
                extractor.extract_title()
            with open(symbol_file, "r") as file:
                reader = csv.reader(file, delimiter=",")
                next(reader)
                for row in reader:
                    # skip first row (header)
                    # symbol stored in first column
                    symbol = row[0]
                    logging.info(symbol)
                    if symbol == "symbol":
                        pass
                    extractor.extract(
                        symbol=symbol,
                        output_format=output_format)
    except KeyboardInterrupt:
        exit

    except Exception as e:
        logging.info(f"{symbol} terminated.", exc_info=True)
        logging.info(e)

    return price_extractor, fundamental_extractor
