## Python Guide

- [Poetry package manager](https://python-poetry.org/)
- [pdoc docs](https://pdoc.dev/docs/pdoc.html)

### Poetry Install

Windows (Powershell)
```sh
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Unix
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry Usage

```sh
poetry shell # activate virtual environment. `exit` to deactivate.
poetry install # install dependencies
poetry run python undis # run undis with python
```
