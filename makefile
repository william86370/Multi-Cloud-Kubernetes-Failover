#Dockerfile vars
python_version=3.9.12-buster
dashboard_app=main.py
healthcheck_app=main.py
init_app=init.py
operator_app=operator.py
healthcheck_port=8080
operator_port=8080
dashboard_port=28015
#Build Target
target=development
#vars
REPO=ghcr.io/william86370
application_version=latest

.PHONY: clean-image
clean-image:
	@echo "+ $@"
	@docker rmi ${IMAGEFULLNAME}  || true

.PHONY: build-cloudwatch-healthcheck-init
build-cloudwatch-healthcheck-init:
	@echo "+ $@"
	@echo "Building cloudwatch-healthcheck-init container"
	@docker build --pull --build-arg PYTHON_APP=${init_app} --build-arg PYTHON_VERSION=${python_version} --build-arg HEALTHCHECK_PORT=${healthcheck_port} -t ${REPO}/cloudwatch-healthcheck-init:${application_version} -f ./Healthcheck/init/Dockerfile ./Healthcheck/init

.PHONY: build-cloudwatch-healthcheck
build-cloudwatch-healthcheck:
	@echo "+ $@"
	@echo "Building cloudwatch-healthcheck container"
	@docker build --pull --build-arg PYTHON_APP=${healthcheck_app} --build-arg PYTHON_VERSION=${python_version} --build-arg HEALTHCHECK_PORT=${healthcheck_port} -t ${REPO}/cloudwatch-healthcheck:${application_version} -f ./Healthcheck/Dockerfile ./Healthcheck

.PHONY: build-cloudwatch-operator
build-cloudwatch-operator:
	@echo "+ $@"
	@echo "Building cloudwatch-operator container"
	@docker build --pull --build-arg PYTHON_APP=${operator_app} --build-arg PYTHON_VERSION=${python_version} --build-arg HEALTHCHECK_PORT=${operator_port} -t ${REPO}/cloudwatch-operator:${application_version} -f ./Operator/Dockerfile ./Operator

.PHONY: build-cloudwatch-dashboard
build-cloudwatch-dashboard:
	@echo "+ $@"
	@echo "Building cloudwatch-dashboard container"
	@docker build --pull --build-arg PYTHON_APP=${dashboard_app} --build-arg PYTHON_VERSION=${python_version} --build-arg HEALTHCHECK_PORT=${dashboard_port} -t ${REPO}/cloudwatch-dashboard:${application_version} -f ./Dashboard/Dockerfile ./Dashboard

.PHONY: push-all
push-all:
	@echo "+ $@"
	@echo "Pushing cloudwatch-healthcheck-init container"
	@docker push ${REPO}/cloudwatch-healthcheck-init:${application_version}
	@echo "Pushing cloudwatch-healthcheck container"
	@docker push ${REPO}/cloudwatch-healthcheck:${application_version}
	@echo "Pushing cloudwatch-operator container"
	@docker push ${REPO}/cloudwatch-operator:${application_version}
	@echo "Pushing cloudwatch-dashboard container"
	@docker push ${REPO}/cloudwatch-dashboard:${application_version}

.PHONY: build-all
build-all: build-cloudwatch-healthcheck-init build-cloudwatch-healthcheck build-cloudwatch-operator build-cloudwatch-dashboard push-all
