include ./setup/main-vars.sh

init:
	pip install --upgrade pip
	pip install wheel
	pip install -r requirements.txt
	pip install -e .

test:
	cd ${PROJECT_FOLDER} && python -m unittest discover -v

coverage:
	python -m pytest \
        --junitxml=junit/test-results.xml \
        --cov=${PROJECT_FOLDER} \
        --cov-report=xml --cov-report=html --cov-report=term

pylint:
	pylint --disable=R,C ${PROJECT_FOLDER} || pylint-exit -efail $$?

bandit:
	bandit -r ${PROJECT_FOLDER}

flake8:
	flake8 || echo "Error"

run-docker:
	cd setup ; ./run-docker-compose.sh

run-demo:
	python botliche/bot.py


.PHONY: init testcd ${PROJECT_FOLDER}
