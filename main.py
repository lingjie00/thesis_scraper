"""Runs the scraper."""
import logging

from finage import extract

"""Set up the logs."""
logging.basicConfig(
    filename="extract.log",
    format='%(asctime)s %(message)s',
    level=logging.INFO)


def main():
    """Runs the scaper.

    relative_path: change relative path if files required is
        stored in different places
    test_flag: if running test symbols only
    csv_flag: if save output as csv files (or json files)
        """
    relative_path = ""
    test_flag: bool = False
    csv_flag: bool = True

    api_file = relative_path+"data/key.ini"

    fundamental_filepath = relative_path+"output/fundamental/"
    price_filepath = relative_path+"output/price/"
    symbol_file = relative_path+"data/LSE_symbols.csv"

    if test_flag:
        # override using test files
        logging.info("Performing test")
        fundamental_filepath = relative_path+"output/test_output/"
        price_filepath = relative_path+"output/test_output/"
        symbol_file = relative_path+"data/symbol_test.csv"

    elif csv_flag:
        # using csv output
        logging.info("Saving to csv file")
        fundamental_filepath = relative_path+"output/csv_output/"
        price_filepath = relative_path+"output/csv_output/"

    price_extractor, fundamental_extractor = extract(
        symbol_file=symbol_file,
        fundamental_filepath=fundamental_filepath,
        price_filepath=price_filepath,
        output_format="csv" if csv_flag else "json",
        api_file=api_file,
        time="1min",
        period="quarter",
        run_price=True,
        run_fundamental=False
    )

    print("Done")


if __name__ == "__main__":
    main()
