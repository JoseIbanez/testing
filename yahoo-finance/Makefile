include ./setup/main-vars.sh

venv:
	uv venv

sync:
	uv sync

test:
	cd ${PROJECT_FOLDER} && python -m unittest discover -v

branch-cleanup:
	git fetch -p
	git branch -v | grep '\[gone\]' | awk '{print $$1}' | xargs -n 1 git branch -D
