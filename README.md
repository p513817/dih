<div align="center">

![cover](./assets/cover.png)
# DIH: Docker Image Handler
**A tool to save and load the docker image tarball file.**

![GitHub License](https://img.shields.io/github/license/p513817/dih)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/p513817/dih/test.yml)
![GitHub tag checks state](https://img.shields.io/github/checks-status/p513817/dih/master)
![GitHub issues](https://img.shields.io/github/issues/p513817/dih)

![Codecov](https://img.shields.io/codecov/c/github/p513817/dih)
![PyPI - Version](https://img.shields.io/pypi/v/dih)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dih)
![PyPI - Downloads](https://img.shields.io/pypi/dm/dih)
![PyPI - Status](https://img.shields.io/pypi/status/dih)

</div>

## Requirements
* `python >3.8`

## Install module with PyPI
```bash
pip install dih
```

## Load docker image with tarball file
* Load docker image with specific folder or file
    ```bash
    dih load -f ./archives
    ```
* Load docker image with manual selection
    ```bash
    python3 src/main.py load -f ./archives --select
    ```
* Load docker image with specific folder and verify with compose file.
    ```bash
    dih load -f ./archives -c <path/to/compose>
    ```
## Save docker image with tarball file
* Save docker image into tarball file.
    ```bash
    dih save -f ./archives
    # Select the index of the docker images
    ```
* Save specific docker image into tarball file.
    ```bash
    # dih save -f ./archives -inc <include keys> -exc <exclude keys>
    dih save -f ./archives -inc innodisk -exc none
    ```

# For Developer
## Requirements
* `python 3.10`
* [Virtualenv, VirtualenvWrapper](./assets/install-venv.md)
* `mkvirtualenv dih`
* `pip install -r requirements.txt`

## Testing
```bash
pytest -v
pytest --doctest-modules --junitxml=junit/test-results.xml --cov=. --cov-report=xml --cov-report=html
```

## Distribute
* Current
    ```bash
    python3 -m pip install --upgrade build
    sudo apt install python3.10-venv
    python3 -m build
    twine upload dist/*
    ```
* Legacy
    ```bash
    python setup.py sdist bdist_wheel
    pip3 install --force-reinstall dist/dih-*.whl
    twine upload dist/*
    ```
