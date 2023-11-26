# [just](https://github.com/casey/just) 를 위한 파일이다.
# just가 설치됐다면 `just run`, `just doc`과 같이 사용할 수 있다.

# list of just commands
default:
	@just --list --unsorted

# run project
run:
	poetry run python undis.py

# start documentation server
doc:
	poetry run pdoc undis

package:
	poetry run pyinstaller -y undis.spec

packaged-run:
	./dist/undis/undis
