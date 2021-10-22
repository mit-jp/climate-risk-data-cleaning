# Joint Program Data Cleaning

Scripts to clean data for use by the [MIT Joint Program on the Science and Policy of Global Change](https://globalchange.mit.edu).

# Setup (macOS)

Install the latest version of python and [`poetry`](https://python-poetry.org) (a python dependency manager)

```
brew install python
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
```

From the root directory of this project, install its dependencies using poetry

```
poetry install
```

## Run code from IDE

From your IDE, select the python interpreter installed by `poetry`. It should be in a directory that looks like `~/Library/Caches/pypoetry/virtualenvs/joint-program-data-cleaning-<random-string>-py3.9/bin` where `<random-string>` will differ for your install.

## Run code from command line

Enter the virtual environment that contains your python dependencies, then scripts as you normally would

```
poetry shell
python your_script.py
```