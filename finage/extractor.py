"""Defines the base class extractor."""
import json
import csv
from datetime import datetime
import logging
from abc import ABCMeta, abstractmethod


class Extractor(metaclass=ABCMeta):
    """A base class extractor."""
    _site: str  # defines the website link to extract
    _api: str   # stores the API needed to login
    _filepath: str  # stores the export path

    def __init__(self, site: str, api: str, filepath: str):
        """Initiate

        params:
            site: API request website
            api: API key
            filepath: path to store the output file
        """
        self.site = site
        self.api = api
        self.filepath = filepath

    @property
    def site(self):
        """API request website."""
        return self._site

    @property
    def api(self):
        """Return API key."""
        return self._api

    @api.setter
    def api(self, key: str):
        """Set API key."""
        self._api = key

    @property
    def filepath(self):
        """Return path to store output files."""
        return self._filepath

    @filepath.setter
    def filepath(self, path: str):
        """Check if filepath is valid before setting."""
        if path[-1] != "/":
            path += "/"
        self._filepath = path

    def to_json(self, content: str, filename: str):
        """Saves the content to json."""
        if filename[:-5] == ".json":
            filename = filename[:-5]
        filename += " " + str(datetime.now()) + ".json"
        with open(f"{self.filepath}{filename}", "w") as file:
            out = json.dumps(content)
            file.write(out)

        logging.info(f"{filename} written")

    @abstractmethod
    def to_csv(self, content: str):
        """Saves the content to a single unified csv."""
        pass

    @abstractmethod
    def extract_title(self):
        """Extract title for csv format."""

    def check_header(self, path: str):
        """Check if csv file has header."""
        with open(path, "r") as file:
            first_line = file.readline()
            if not first_line:
                return False
            return csv.Sniffer().has_header(first_line)

    @abstractmethod
    def extract(self, symbol: str, output_format: str):
        """Extracts the symbol."""

    @abstractmethod
    def check_content(content: str):
        """Check if content is valid."""
        pass

    @abstractmethod
    def generate_link(self, symbol: str):
        """Generate GET link."""
        pass
