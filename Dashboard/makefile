#Dockerfile vars
python_version=3.9.12-buster
healthcheck_port=28015
python_app=main.py
#vars
IMAGENAME=cloudwatch-dashboard
REPO=ghcr.io/william86370
application_version=latest
IMAGEFULLNAME=${REPO}/${IMAGENAME}:${application_version}

.PHONY: help build push all

help:
	    @echo "Makefile arguments:"
	    @echo ""
	    @echo "python_version - Python Container Version"
	    @echo "healthcheck_port - Healthcheck Port"
	    @echo "application_version - Container Version"
	    @echo "python_app - Bundled python Application"
	    @echo ""
	    @echo "Makefile commands:"
	    @echo "build"
	    @echo "push"
	    @echo "all"

.DEFAULT_GOAL := all

build:
	    @docker build --pull --build-arg PYTHON_APP=${python_app} --build-arg PYTHON_VERSION=${python_version} --build-arg HEALTHCHECK_PORT=${healthcheck_port} -t ${IMAGEFULLNAME} .


push:
	    @docker push ${IMAGEFULLNAME}

all: build push

.PHONY: clean-image
clean-image:
	@echo "+ $@"
	@docker rmi ${IMAGEFULLNAME}  || true
.PHONY: build-containers
build-containers:
	@echo "Building All Operator Containers"
	@echo "\nBuild cloudwatch-healthcheck"
	@echo ""
	@docker build -t ${REPO}/cloudwatch-healthcheck:${application_version} -f ./Healthcheck/Dockerfile ./Healthcheck
	@echo "\nBuild cloudwatch-dashboard"
	@echo ""
	@docker build -t ${REPO}/cloudwatch-dashboard:${application_version} -f ./Dashboard/Dockerfile ./Dashboard
	@echo "\nBuild cloudwatch-operator"
	@echo ""
	@docker build -t ${REPO}/cloudwatch-operator:${application_version} -f ./Operator/Dockerfile ./Operator