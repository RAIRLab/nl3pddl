# NL3PDDL

## Dependencies

The codebase has only been tested on Linux, specifically WSL2 running Ubuntu. 
* [Python >=3.10](https://www.python.org/downloads/)
* [Poetry Package Manager for python](https://python-poetry.org/)
* [CMake](https://cmake.org/) (for compiling VAL)

### Submodules
* [numberlink](https://github.com/KCL-Planning/numberlink) (git submodule) 
* [VAL](https://github.com/KCL-Planning/VAL) (git submodule) 

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

### Ensure you have installed all required submodules:
```bash
git submodule update --init --recursive
```

Ensure VAL is compiled to the proper location `submodules/VAL/build/bin` 
(note that you can't use the default build script as it puts the binaries in a different location):
```bash
cd submodules/VAL
mkdir build
cd build
cmake ..
make
cd ../../../
```

### Set API keys in .env file (only required to run full experiments)
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

