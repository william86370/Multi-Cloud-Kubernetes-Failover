# CloutWatch-Healthcheck
#
# Copyright (C) 2022 William Wright <
import os

from flask import Flask
import requests

app = Flask(__name__)


@app.route("/")
def hello():
    return "OK"


@app.route("/get_cloud_provider")
def get_cloud_provider():
    """
    Using Low Level API to get cloud provider
    :return: cloud provider
    Use IMDSv2 to get cloud provider
    """
    path = 'latest/meta-data/instance-id'
    url = f'http://169.254.169.254/{path}'
    r = requests.get(url)
    return r.content.decode('utf-8')


@app.route('/healthz')
def healthz():
    return "OK"


if __name__ == "__main__":
    print("Starting CloutWatch-Healthcheck Deamonset")
    # Get port from environment variable or choose 8080 as local Healthcheck port if no environment variable found
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
