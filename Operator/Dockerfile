FROM ubuntu:20.04
# Install packages
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
# Install python3
RUN apt-get install -y python3
# install python3-pip
RUN apt-get install -y python3-pip
# Copy requirements.txt to /tmp
COPY requirements.txt /tmp/requirements.txt
# Install requirements
RUN pip3 install -r /tmp/requirements.txt
# Copy Operator.py to /tmp
COPY Operator.py /tmp/Operator.py
# set Operator.py as executable
RUN chmod +x /tmp/Operator.py
# Entrypoint
ENTRYPOINT ["/tmp/Operator.py"]
