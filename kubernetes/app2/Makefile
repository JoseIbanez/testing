branch-cleanup:
	git fetch -p
	git branch -v | grep '\[gone\]' | awk '{print $$1}' | xargs -n 1 git branch -D


helm:
	./setup/make_helm.sh

helm-publish:
	./setup/make_helm.sh upload

helm-test:
	helm lint charts
	helm install test-lgst charts  --dry-run

helm-install:
	helm lint charts
	helm delete test-lgst || echo "."
	sleep 1
	helm upgrade --install test-lgst ./charts/

.PHONY: test

