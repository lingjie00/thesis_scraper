"""Extract fundamental data from Finage."""
import logging
import json
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
