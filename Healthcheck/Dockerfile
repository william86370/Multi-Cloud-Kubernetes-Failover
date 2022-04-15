FROM python:3-alpine
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY main.py /app
EXPOSE 8080
CMD ["python", "main.py"]