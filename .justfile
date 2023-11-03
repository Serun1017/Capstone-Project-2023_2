# [just](https://github.com/casey/just) 를 위한 파일이다.
# just가 설치됐다면 `just run`, `just doc`과 같이 사용할 수 있다.
default:
	@just --list --unsorted

run:
	poetry run python undis

doc:
	poetry run pdoc undis
