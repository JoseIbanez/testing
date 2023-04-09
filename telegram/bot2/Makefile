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


pkg:
	./setup/make_whl.sh

pkg-publish:
	./setup/make_whl.sh upload

docker:
	./setup/docker-build.sh

docker-publish:
	./setup/docker-build.sh publish-aws

helm-install:
	helm delete ${CHART_NAME} || echo "delete error"
	sleep 1
	helm install ${CHART_NAME} ./helm-chart/${CHART_NAME}

run-demo:
	python stock_price_bot/bot.py

run:
	gunicorn -b 0.0.0.0:8008 acelink_server.app:app	

deploy-service:
	cd setup ;  ./deploy-service.sh


.PHONY: init testcd ${PROJECT_FOLDER}
