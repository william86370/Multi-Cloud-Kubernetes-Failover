# CloutWatch-Healthcheck
#
# Copyright (C) 2022 William Wright <
import os

from flask import Flask
import requests

app = Flask(__name__)


@app.route("/")
def default():
    return "CloudWatch-Healthcheck is running Try /healthcheck"


#
# @app.route("/get_cloud_provider")
# def get_cloud_provider():
#     """
#     Using Low Level API to get cloud provider
#     :return: cloud provider
#     Use IMDSv2 to get cloud provider
#     """
#     # Check if cloud provider is AWS
#     try:
#         path = 'latest/dynamic/instance-identity/document'
#         url = f'http://169.254.169.254/{path}'
#         response = requests.get(url)
#         if response.status_code == 200:
#             # Check Availability Zone
#             availability_zone = response.json()['availabilityZone']
#             if availability_zone.startswith('us-east-'):
#                 return 'AWS'
#             else:
#                 return 'Azure'
#     except:
#         return "Unknown"


@app.route('/healthcheck')
def healthcheck():
    return "OK"


if __name__ == "__main__":
    print("Starting CloudWatch-Healthcheck")
    # Get port from environment variable or choose 8080 as local Healthcheck port if no environment variable found
    port = int(os.getenv("PORT", 8080))
    print(f"Starting Healthcheck on port {port}")
    app.run(host='0.0.0.0', port=port)
