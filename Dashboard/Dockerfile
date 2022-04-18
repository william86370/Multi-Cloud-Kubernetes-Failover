ARG PYTHON_VERSION=3.9.12-buster
ARG HEALTHCHECK_PORT=28015
ARG PYTHON_APP=main.py
FROM python:${PYTHON_VERSION}
ARG HEALTHCHECK_PORT
ARG PYTHON_APP
LABEL org.opencontainers.image.authors = "william86370"
LABEL org.opencontainers.image.created = "2022-04-17"
LABEL org.opencontainers.image.documentation = "https://github.com/william86370/Multi-Cloud-Kubernetes-Failover"
LABEL org.opencontainers.image.version = "1.0"
LABEL org.opencontainers.image.title = "Cloudwatch Dashboard"
LABEL org.opencontainers.image.description = "Exposes a healthcheck endpoint to check the health of the Kubernetes node"

RUN mkdir /app
WORKDIR /app
# Copy Python requirements
COPY requirements.txt /app
RUN pip install -r requirements.txt
# Copy the init script
COPY ./${PYTHON_APP} /app/${TARGET_APP}
# Expose the default healthcheck port
ENV PORT=${HEALTHCHECK_PORT}
EXPOSE ${HEALTHCHECK_PORT}
ENV PYTHON_APP=${PYTHON_APP}
CMD python3 ${PYTHON_APP}