# finage

[![package](https://github.com/lingjie00/thesis_scraper/actions/workflows/project-actions.yml/badge.svg)](https://github.com/lingjie00/thesis_scraper/actions/workflows/project-actions.yml)
[![Docker](https://github.com/lingjie00/thesis_scraper/actions/workflows/docker-actions.yml/badge.svg)](https://github.com/lingjie00/thesis_scraper/actions/workflows/docker-actions.yml)

# Project overview

scraper for thesis data source

# Folder structure

- [docs](/docs): includes the methodology and documentations 
- [notebooks](/notebooks): includes sample codes in jupyter notebooks format
- [finage]: source codes

# Local development

install [miniconda](https://docs.conda.io/en/latest/miniconda.html)
and create new virtual environment

```bash
# create new environment, replace ```finage``` with the env name
conda create -n finage python==3.10

# activate the new environment
conda activate finage

# install essential packages and this repo package
pip install -r requirements.txt
```
