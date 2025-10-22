# NL3PDDL

## Dependencies

The codebase has only been tested on Linux, specifically WSL2 running Ubuntu.

### Required
* [Python 3.13 (free-threaded)](https://www.python.org/downloads/) - For optimal performance with multithreading
* [uv](https://astral.sh/uv) - Fast Python package manager
* [CMake](https://cmake.org/) - For compiling VAL submodule
* System packages: `build-essential`, `graphviz`, `graphviz-dev`

### Git Submodules
* [numberlink](https://github.com/thomasahle/numberlink) - For numberlink problem generation
* [VAL](https://github.com/KCL-Planning/VAL) - PDDL plan validator

## Installation

### 1. Install uv package manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone repository with submodules

```bash
git clone --recursive https://github.com/yourusername/nl3pddl.git
cd nl3pddl
```

If you already cloned without submodules:
```bash
git submodule update --init --recursive
```

### 3. Install system dependencies

```bash
sudo apt-get update
sudo apt-get install -y cmake build-essential graphviz graphviz-dev
```

### 4. Set up Python environment with free-threaded Python

Create a virtual environment with Python 3.13 free-threaded (no GIL):
```bash
uv venv --python 3.13t
```

Install Python dependencies:
```bash
uv sync
```

### 5. Build VAL submodule

```bash
cd submodules/VAL
mkdir -p build
cd build
cmake ..
make
cd ../../../
```

### 6. Configure API keys (required for running experiments)

```bash
cp .env_template .env
```

Edit the `.env` file and add your API keys for the LLM providers you want to use.
Make sure that you call, uv is weird with env variables from .env
```bash
export PYTHON_GIL=0
```

### 7. Verify installation

Test that GIL is disabled (should print `False`):
```bash
uv run python scripts/test_gil_enabled.py
```

Test all problem generators:
```bash
uv run python run.py -t
```

## Usage

### Running Experiments

Run the main script to execute experiments and produce a `results.csv` file:

```bash
uv run python run.py -r
```

### Experiment Configuration

Modify experiment parameters in `experiment_config.yaml` to customize:
- Models to test
- Problem domains
- Description strategies
- Feedback pipelines
- Number of trials

### Generating Plots

After experiments complete, generate visualization plots:

```bash
uv run python run.py -p
```

This will use the latest `results.csv` file to create figures.

### Testing Problem Generators

Test all problem generators (runs tests for sizes 1-10):
```bash
uv run python run.py -t
```

Test a specific generator with default size (5):
```bash
uv run python run.py -t blocks
```

Test a specific generator with custom size:
```bash
uv run python run.py -t blocks 8
```

Available generators: `blocks`, `bookseller`, `checkers-jumping`, `elevators`, `flow`, `miconic`, etc.
