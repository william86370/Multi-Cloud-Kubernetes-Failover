FROM python:3-alpine
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY main.py /app
EXPOSE 8080
LABEL org.opencontainers.image.description = "Cloudwatch Healthcheck: Healthcheck for the Cloudwatch API"
CMD ["python", "main.py"]

# docker run --rm -it -p 8080:8080 ghcr.io/william86370/cloudwatch-daemon:latest