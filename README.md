# CI Workflow Example: geodata-calibration

This repository shows a minimal Continuous Integration setup using GitHub Actions. 

## Repository Structure
```bash
├── LICENSE
├── README.md
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
├── src
│   └── geodata_calibration
│       ├── __init__.py
│       └── utils.py
├── .github
│   └── workflows
│       ├── python-app.yml
└── tests
    └── test_utils.py
```

### 1. `.github/workflows/python-app.yml`
This file defines the steps of the CI workflow, including setting up a Python environment, installing dependencies, linting the code, and running tests.

### 2. `src/geodata_calibration/utils.py`
It contains the core project code. In this example, it includes functions for reprojection and clipping of geospatial data.

### 3. `tests/test_utils.py`
This file contains test cases for `src/geodata_calibration/utils.py`, using `pytest` to verify that the functions work as expected.

### 4. `requirements.txt`
This file lists the dependencies. The CI workflow uses it to prepare the virtual environment during test execution.

### 5. `.pre-commit-config.yaml`
This file configures pre-commit hooks for the repository, ensuring that code is automatically linted with `Black` and `Isort` before each commit.

### 6. `pyproject.toml`
This file configures tools and options needed for the build system, dependency management, and testing of the project.

