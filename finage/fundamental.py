"""Extract fundamental data from Finage."""
import csv
import logging

import requests
from extractor import Extractor


class Fundamental(Extractor):
    """Extract fundamental data from Finage.

    params:
        _site: base site to extract data from
        _period: frequency of data, either quarter or annual
    """
    _site: str = "https://api.finage.co.uk/income-statement/"
    _period: str  # period to extract (quarter or anuual)

    def __init__(self, api: str, filepath: str, period: str):
        """Initiate.

        params:
            api: API key
            filepath: filepath to store the output files
            period: either quarter or annual fundamental
            data
        """
        self.api = api
        self.filepath = filepath
        self.period = period

    @property
    def period(self):
        """Get the frequency of data."""
        return self._period

    @period.setter
    def period(self, period: str):
        """Check if the period requested is valid."""
        assert(period in ("quarter", "annual"))
        self._period = period

    @staticmethod
    def check_content(content: str):
        """Check if content is valid."""
        logging.debug(content)
        return "error" not in content

    def to_csv(self, content: str, values: bool):
        """Saves the content to csv."""
        if not content:
            logging.info(f"content is empty {content}")
            return self

        path = self._filepath + "fundamental.csv"

        with open(path, "a") as file:
            """Default: append to CSV"""
            writer = csv.writer(file)
            counter = 0
            if values:
                for data in content:
                    logging.debug(f"Writing row {counter}")
                    writer.writerow(data.values())
                    counter += 1
            elif not values and not self.check_header(path):
                # only write title if header does not exist
                logging.debug("Write header")
                writer.writerow(content[0].keys())
            else:
                logging.info("Nothing is done")

    def generate_link(self, symbol: str):
        """Generate API request link."""
        link = self.site + symbol + ".L" +\
            "?&period=" + self.period +\
            "&apikey=" + self.api
        logging.debug(f"Request link {link}")
        return link

    def extract(self, symbol: str, output_format: str,
                values: bool = True):
        """Main function user interact with to extract data."""
        link = self.generate_link(symbol)
        response = requests.get(link)
        content = response.json()

        if not self.check_content(content):
            raise NotImplementedError(f"{symbol} not found: {content}")

        if output_format == "json":
            self.to_json(content, symbol)
        elif output_format == "csv":
            self.to_csv(content, values)
        return self

    def extract_title(self):
        """Extract headers for CSV output."""
        symbol = "BP"  # reference symbol

        self.extract(symbol, output_format="csv",
                     values=False)
