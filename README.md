# NL3PDDL

## Dependencies

The codebase has only been tested on Linux, specifically WSL2 running Ubuntu. 
* [Python >=3.10](https://www.python.org/downloads/)
* [Poetry Package Manager for python](https://python-poetry.org/)

## Install 

### (Optionally) Setup a virtual environment 
preferred name is `.venv` as it is in the `.gitignore`. Set poetry to use this venv.
```bash
python3 -m venv .venv

```

### Install all python deps:
```bash
poetry install
```

### Set API keys in .env file
```bash
cp .env_template .env
```
Fill out this file with relevant API keys

## Run

Run the driver script to produce a `results.csv` file
Experiment parameters and grid can be tweaked in the
`experiment_config.yaml` file.
```bash
python driver.py
```

Once the experiments have been run, you can generate figures using the driver
with a `-p` flag. This will use the latest `results.csv` file.
```bash
python driver.py
```

