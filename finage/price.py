"""Extracts price data from Finage."""
import csv
import logging
from multiprocessing import Pool, cpu_count

import requests
from extractor import Extractor


class Price(Extractor):
    """Price extractor.

    params:
        _site: the base API site to extract
        _time: frequency of data, check self.time for
        possible timings
        _start: start date for extraction
        _to: end date for extraction
        _day_interval, _month_interval, _year_interval:
            determines how frequent to extract the data.
            Since Finage has an API limit of 5000 requests,
            this interval is only useful for frequency lower
            than 1 day (for 1day frequency, we can extract
                    5000 requests/365days=13years data,
                    sufficient for our needs)
    """
    _site: str = "https://api.finage.co.uk/agg/stock/global/uk/"
    _time: str  # frequency of data
    _start: str = "2010-01-01"
    _to: str = "2022-03-01"
    _day_interval: dict = {
        "1min": 3, "5min": 17, "15min": 31, "30min": 31,
        "45min": 31, "1h": 31, "2h": 31, "4h": 31}
    _month_interval: dict = {
        "1min": 1, "5min": 1, "15min": 1, "30min": 3,
        "45min": 5, "1h": 6, "2h": 12, "4h": 12}
    _year_interval: dict = {
        "1min": 1, "5min": 1, "15min": 1, "30min": 1,
        "45min": 1, "1h": 1, "2h": 1, "4h": 2}

    def __init__(self, api: str, filepath: str, time: str):
        """Initiate extractor.

        params:
            api: API key
            filepath: path to save the output files
            time: frequency to extract the data, refer to
                self.time
        """
        self.api = api
        self.filepath = filepath
        self.time = time

    @property
    def time(self):
        """Frequency of extraction."""
        return self._time

    @time.setter
    def time(self, time: str):
        """Check if the requested frequency is allowed."""
        valid_time = ["1min", "5min", "15min", "30min", "45min",
                      "1h", "2h", "4h", "1day", "1week", "1month"]
        assert(time in valid_time)
        self._time = time

    @property
    def start(self):
        """Start date."""
        return self._start

    @property
    def to(self):
        """End date."""
        return self._to

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

        try:
            symbol = content["symbol"]
            price = content["results"]
        except KeyError:
            return

        path = self.filepath + f"price_{self.time}.csv"

        with open(path, "a") as file:
            """Always append to the CSV file."""
            writer = csv.writer(file)
            counter = 0
            if values:
                for data in price:
                    logging.debug(f"Writing row {counter}")
                    data = [symbol] + list(data.values())
                    writer.writerow(data)
                    counter += 1
                counter += 1
            elif not values and not self.check_header(path):
                # only write title if header does not exist
                logging.debug("Write header")
                data = ["symbol"] + list(price[0].keys())
                writer.writerow(data)
            else:
                logging.info(f"Nothing is done for {symbol}")

    def generate_link(self, symbol: str):
        """Generates the API request link."""
        links = []
        if self.time in ["1day", "1week", "1month"]:
            # only require 1 extraction
            link = self.site + symbol +\
                "/" + self.time + "/" +\
                self.start + "/" + self.to +\
                "?apikey=" + self.api + "&limit=5000"
            logging.debug(f"Request link {link}")
            links.append(link)
        else:
            current_date = self.start
            # require iterative extraction
            # but can only get past 1 years due to Finage
            # only storing that length of high frequent data
            for year in range(
                    2020, 2023, self._year_interval[self.time]):
                year_str = str(year).zfill(4)
                for month in range(
                        1, 12, self._month_interval[self.time]):
                    month_str = str(month).zfill(2)
                    for day in range(
                            1, 31, self._day_interval[self.time]):
                        day_str = str(day).zfill(2)
                        next_date = f"{year_str}-{month_str}-{day_str}"
                        link = self.site + symbol +\
                            "/" + self.time + "/" +\
                            current_date + "/" + next_date +\
                            "?apikey=" + self.api + "&limit=5000"
                        logging.debug(f"Request link {link}")
                        links.append(link)
                        current_date = next_date
        return links

    def retrieve_link(self, link: str):
        """Retrieve the requested link."""
        response = requests.get(link)
        content = response.json()
        return content

    def extract(self, symbol: str, output_format: str,
                values: bool = True):
        """Extract the data. Main method user will interact with."""
        # link
        links = self.generate_link(symbol)
        with Pool(cpu_count()) as p:
            contents = p.map(self.retrieve_link, links)
        for content in contents:

            if not self.check_content(content):
                logging.info(f"{symbol} not found: {content}")

            if output_format == "json":
                self.to_json(content, symbol)
            elif output_format == "csv":
                self.to_csv(content, values)

        logging.info(f"{symbol} price extracted")

    def extract_title(self):
        """Useful for CSV files, extract headers."""
        symbol = "BP"  # sample pull this symbol for header
        self.extract(symbol, output_format="csv",
                     values=False)
