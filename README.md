# Undefined Image Search

## Code Style

VSCode 확장 Ruff를 설치해서 자동으로 코드 정리하게 하자.
Docstring(파이썬 기능)으로 코드를 설명하고 pdoc으로 읽기 좋은 문서를 생성하자.

## Python Guide

### Poetry

가상 환경은 docker처럼 파이썬이 패키지를 찾는 위치를 시스템으로부터 독립시키고, 여러 컴퓨터에서 작업을 할때 서로 다른 환경이 아니도록 도와준다.
이런 가상 환경을 관리해주는 매니저로 Poetry를 사용하도록 하자.

#### Install

Windows (Powershell)
```sh
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Unix
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

#### Config

Poetry는 기본으로 시스템 홈 폴더에 가상 환경을 만들어 주는데 VSCode 같은 에디터와의 가상 환경 호환을 위해서는 프로젝트 폴더에 만드는 것이 유리하다.

```sh
poetry config virtualenvs.in-project true # Make virtual environment in project folder
poetry config virtualenvs.path "./.venv" # Virtual environment path is .venv
```

VSCode를 이용한다면 LSP와 연결을 위해 `Python: Select Interpreter`를 .venv/bin/python으로 지정해주자.

#### Usage

```sh
# pyproject.toml을 읽고 가상환경에 패키지를 설치한다.
# 패키지가 바뀔 때 마다 한번씩 실행해줘야한다.
poetry install

# 터미널에서 프로젝트와 관련된 일을 할 때 가상환경을 활성화 하는 명령어다.
# `exit` 명령어를 치면 가상환경을 종료한다.
poetry shell

# `poetry shell` 없이 명령어를 실행하려면 `poetry run`으로 해주면 된다.
poetry run python undis # run `python undis` in virtual environment
poetry run pdoc undis # run `pdoc undis` in virtual environment
```

### pdoc

소스코드를 직접 읽게 하는것 만큼 시간을 낭비하는 협업이 있을까? 파이썬의 docstring에서 문서를 자동생성해주는 pdoc을 사용하자.

```sh
# 문서 서버 열기
pdoc undis
# Poetry를 이용해 가상환경에서 문서 서버 열기
poetry run pdoc undis
```

## Links

- Poetry [[github]](https://github.com/python-poetry/poetry) [[docs]](https://python-poetry.org/docs/) [[website]](https://python-poetry.org/)
- pdoc [[github]](https://github.com/mitmproxy/pdoc) [[docs]](https://pdoc.dev/docs/pdoc.html) [[website]](https://pdoc.dev/)