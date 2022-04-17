ARG PYTHON_VERSION=3.9.12-buster
ARG HEALTHCHECK_PORT=8080
FROM python:${PYTHON_VERSION}

LABEL org.opencontainers.image.authors = "william86370"
LABEL org.opencontainers.image.created = "2022-04-17"
LABEL org.opencontainers.image.documentation = "https://github.com/william86370/Multi-Cloud-Kubernetes-Failover"
LABEL org.opencontainers.image.version = "1.0"
LABEL org.opencontainers.image.title = "Cloudwatch Healthcheck init"
LABEL org.opencontainers.image.description = "Anotates the host node with the Cloud-Provider"

RUN mkdir /app
WORKDIR /app
# Copy Python requirements
COPY requirements.txt /app
RUN pip install -r requirements.txt
# Copy the init script
COPY init.py /app
# Expose the default healthcheck port
ENV PORT=${HEALTHCHECK_PORT}
EXPOSE ${HEALTHCHECK_PORT}

CMD ["python3", "init.py"]