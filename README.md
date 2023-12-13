<div align="center">

![cover](https://github.com/p513817/dih/blob/master/assets/cover.png?raw=true)
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
* python >=3.8
* [Virtualenv, VirtualenvWrapper](./assets/install-venv.md)

## Install module with PyPI
```bash
mkvirtualenv dih
pip install dih
```

## Load docker image with tarball file

* Load docker image with specific folder or file
    ```bash
    dih load -f ./archives
    ```
* Load docker image with manual selection
    ```bash
    dih load -f ./archives --select
    ```
    <details>
    <summary>Sample</summary>
    <br>
        <p>
        <img src='https://github.com/p513817/dih/blob/master/assets/dih-load-select.png?raw=true' width='auto' height=200px alt>
        <br>
        <em>Enter the index of the docker images...</em>
        </p>
    </details>
    <br>

* Load docker image with specific folder and verify with compose file.
    ```bash
    dih load -f ./archives -c <path/to/compose>
    ```
    <details>
    <summary>Sample</summary>
    <br>
        <p>
        <img src='https://github.com/p513817/dih/blob/master/assets/dih-load-compose.png?raw=true' width='auto' height=250px alt>
        <br>
        <em>Verify with compose file and only load the verified indexes...</em>
        </p>
    </details>
    <br>
    

## Save docker image into tarball file
* Save docker image into tarball file.
    ```bash
    dih save -f ./archives
    ```
* Filter with specific rule, includes something and excludes something.
    ```bash
    dih save -f ./archives -inc innodisk -exc none
    ```
    
    <details>
    <summary>Sample</summary>
    <br>
        <p>
        <img src='https://github.com/p513817/dih/blob/master/assets/dih-save-with-rule.png?raw=true' width='auto' height=200px alt>
        <br>
        <em>dih save -f ./archives -inc rtsp -exc none...</em>
        </p>
    </details>
    <br>

## More detail
* `dih load --help`
    ```bash
    Usage: dih load [OPTIONS]
    
    Options:
    -f, --folder PATH        Path to the folder.  [required]
    -c, --compose-file PATH  Path to compose file.
    -s, --select             Select by index.
    --debug                  Only display the information.
    --help                   Show this message and exit.
    ```
* `dih save --help`
    ```bash
    Usage: dih save [OPTIONS]

    Options:
    -f, --folder TEXT      Path to the folder.  [required]
    -inc, --includes TEXT  Include keys.
    -exc, --excludes TEXT  Exclude keys.
    --debug                Only display the information.
    --help                 Show this message and exit.
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
```bash
python3 -m pip install --upgrade build
sudo apt install python3.10-venv
python3 -m build
twine upload dist/*
```
