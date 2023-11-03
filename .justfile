default:
	@just --list --unsorted

run:
	poetry run python undis

doc:
	poetry run pdoc undis
