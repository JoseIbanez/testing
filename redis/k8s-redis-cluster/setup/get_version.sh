#!/bin/sh
set -e


if [[ "$OSTYPE" == "darwin"* ]]; then
        GNUSED="gsed"
else
        GNUSED="sed"
fi

VERSION_FILE="./setup/_version.py"
FULVER=$(head -n 1 $VERSION_FILE)
SEMVER=`echo $FULVER | $GNUSED  -n 's/[^0-9]*\([0-9\.]\+\).*/\1/p'`
echo "SEMVER: >${SEMVER}<, Last Version: >${FULVER}<"


# Gitlab pipeline
if [ "$CI_COMMIT_TAG" ]; then
    echo "CI_COMMIT_TAG=>$CI_COMMIT_TAG<"
    NEWVERSION=`echo $CI_COMMIT_TAG | $GNUSED -n 's/[^0-9]*\([0-9\.]\+\).*/\1/p'`

elif [ "${CI_PIPELINE_IID}" ]; then
    NEWVERSION="${SEMVER}-dev${CI_PIPELINE_IID}"
fi

# Else (local)
if [ ! "$NEWVERSION" ]
then
      NEWVERSION="${SEMVER}-dev`date +%s`"
fi
echo "New version: >$NEWVERSION<"


# "latest" or "dev" tag selection
if [[ "$CI_COMMIT_BRANCH" == "master" || -n "$CI_COMMIT_TAG" ]]; then
        IMAGE_TAG2="latest"
else
        IMAGE_TAG2="dev"
fi


# To create a dist
echo "__version__ = \"$NEWVERSION\"" > $VERSION_FILE
cat $VERSION_FILE

