# Thesis data scraper

[![package](https://github.com/lingjie00/thesis_scraper/actions/workflows/project-actions.yml/badge.svg)](https://github.com/lingjie00/thesis_scraper/actions/workflows/project-actions.yml)
[![Docker](https://github.com/lingjie00/thesis_scraper/actions/workflows/docker-actions.yml/badge.svg)](https://github.com/lingjie00/thesis_scraper/actions/workflows/docker-actions.yml)

# Project overview

Scraper for thesis data source, currently only supporting
data extraction from Finage.

If you are not modifying the script, focus on `main.py`
where I show how to use the package.

You would require the following files (using the default
file path)

1. ./data/key.ini: storing API key
2. ./data/LSE_symbols.csv: storing the symbols to extract

Please modify the `main.py` if the file name and location is
different from the default.

# Folder structure

- [finage]: source codes

# Local development and requirements

I use the standard packages from Python (request,
configparser, multiprocessing, csv, logging). No external
library is needed.
All Python version >= 3.6 should work. I used Python 3.10
for development.

install [miniconda](https://docs.conda.io/en/latest/miniconda.html)
and create new virtual environment

```bash
# create new environment, replace ```finage``` with the env name
conda create -n finage python==3.10

# activate the new environment
conda activate finage
```
