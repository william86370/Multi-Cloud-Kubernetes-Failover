#Dockerfile vars
python_version=3.9.12-buster
healthcheck_port=8080
python_app=main.py
#vars
IMAGENAME=cloudwatch-healthcheck
REPO=ghcr.io/william86370
application_version=latest
IMAGEFULLNAME=${REPO}/${IMAGENAME}:${application_version}

.PHONY: help build push apply all

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