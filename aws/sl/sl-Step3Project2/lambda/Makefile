include: ../aws_cli/sl_vars.sh

list:
	aws lambda list-functions --max-items 50 | jq '.Functions[].FunctionArn'


build:
	mkdir -p ./dist/
	cd src; zip -r ../dist/lambda.zip .


get:
	aws lambda get-function \
		--function-name ${LAMBDA_NAME}


publish:
	rm -f ./dist/lambda.zip
	cd src; zip -r ../dist/lambda.zip .
	aws lambda update-function-code \
		--function-name ${LAMBDA_NAME} \
		--zip-file fileb://dist/lambda.zip 

