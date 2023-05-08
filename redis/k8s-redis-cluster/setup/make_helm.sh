#!/bin/bash
set -e

PROJECT_ID=1035
CHART_NAME=otel-msk-collector


# Get $NEWVERSION
. "./setup/get_version.sh"
echo "Helm version: $NEWVERSION"

# Get DOCKER_TAG
if [ -f "./_docker_tag.tmp" ] ; then
    DOCKER_TAG=`cat ./_docker_tag.tmp`
else
    DOCKER_TAG=$NEWVERSION
fi
echo "Docker tag: $DOCKER_TAG"

# Get HELM channel
if [[ "$CI_COMMIT_BRANCH" == "master" || -n "$CI_COMMIT_TAG" ]]; then
        CHANNEL="master"
else
        CHANNEL="dev"
fi


helm package ./helm-chart/${CHART_NAME} -d ./helm-chart/ --app-version $DOCKER_TAG --version $NEWVERSION 


# To upload to git registry
if [[ "$1" == "upload" ]]; then

    curl --request POST \
        --form "chart=@./helm-chart/${CHART_NAME}-${NEWVERSION}.tgz" \
        --user "__token__:${CI_JOB_TOKEN:-$LOCAL_TOKEN}" \
        "https://gitlab-ucc.tools.aws.vodafone.com/api/v4/projects/${CI_PROJECT_ID:-$PROJECT_ID}/packages/helm/api/${CHANNEL}/charts"

fi
