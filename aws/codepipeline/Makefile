include .env.local

.DEFAULT_GOAL := all

all: build deploy
.PHONY: all

setup:
	# create environment specific param and conf files here
	envsubst < .params.template > .params
	$(shell cat .params | sed 's/\r//g' | sed 's/\n//g' | sed 's/\,//g' > .params)
	envsubst < .conf.template > .conf

.PHONY: setup

init: setup
	aws cloudformation deploy \
		--template-file template-prereqs.yaml \
		--stack-name "${ACCT_PREFIX}-${ENVIRONMENT}-${APPNAME}-init" \
		--capabilities CAPABILITY_NAMED_IAM \
		--region ${AWS_REGION} \
		--profile ${AWS_PROFILE} \
		--parameter-overrides $(shell cat .params)

.PHONY: init

pipeline: setup
	sam build \
		--template-file template-pipeline.yaml \
		--region ${AWS_REGION} \
		--profile ${AWS_PROFILE} \
		${SAM_DEBUG_OPTION}

	sam package \
		--template-file .aws-sam/build/template.yaml \
		--output-template-file template-out.yaml \
		--s3-bucket ${BUILD_BUCKET} \
		--s3-prefix cfn \
		--profile ${AWS_PROFILE} \
		--region ${AWS_REGION} \
		${SAM_DEBUG_OPTION}

	sam deploy \
		--template-file template-out.yaml \
		--s3-bucket ${BUILD_BUCKET} \
		--s3-prefix cfn \
		--stack-name "${ACCT_PREFIX}-${ENVIRONMENT}-${APPNAME}-pipeline" \
		--capabilities CAPABILITY_NAMED_IAM \
		--region ${AWS_REGION} \
		--profile ${AWS_PROFILE} \
		--parameter-overrides $(shell cat .params) \
		${SAM_DEBUG_OPTION}

.PHONY: pipeline

build: setup
	sam build \
		--region ${AWS_REGION} \
		--profile ${AWS_PROFILE} \
		${SAM_DEBUG_OPTION}

.PHONY: build

deploy: setup build
	sam package \
		--template-file .aws-sam/build/template.yaml \
		--output-template-file template-out.yaml \
		--s3-bucket ${BUILD_BUCKET} \
		--s3-prefix cfn \
		--profile ${AWS_PROFILE} \
		--region ${AWS_REGION} \
		${SAM_DEBUG_OPTION}

	sam deploy \
		--template-file template-out.yaml \
		--s3-bucket ${BUILD_BUCKET} \
		--s3-prefix cfn \
		--stack-name "${ACCT_PREFIX}-${ENVIRONMENT}-${APPNAME}-resources" \
		--capabilities CAPABILITY_NAMED_IAM \
		--profile ${AWS_RUN_PROFILE} \
		--region ${AWS_REGION} \
		--parameter-overrides $(shell cat .params) \
		${SAM_DEBUG_OPTION}

.PHONY: deploy

run: setup build
	sam local start-api \
		--port ${SAM_API_PORT} \
		--docker-volume-basedir ${WORKINGDIR}/.aws-sam/build \
		--debug \
		--debug-port ${SAM_DEBUG_PORT} \
		--region ${AWS_REGION} \
		--profile ${AWS_RUN_PROFILE} \
		--parameter-overrides $(shell cat .params) \
		${SAM_DEBUG_OPTION}

.PHONY: run
