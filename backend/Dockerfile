# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# open ai api key
ENV OPENAI_API_KEY $OPENAI_API_KEY

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
WORKDIR /app
ADD . /app