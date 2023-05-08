branch-cleanup:
	git fetch -p
	git branch -v | grep '\[gone\]' | awk '{print $$1}' | xargs -n 1 git branch -D


helm:
	./setup/make_helm.sh

helm-publish:
	./setup/make_helm.sh upload

helm-test:
	helm lint charts
	helm install redis-cluster charts  --dry-run

helm-install:
	helm lint charts
	helm delete redis-cluster || echo "."
	sleep 1
	helm upgrade --install redis-cluster ./charts/

.PHONY: test

