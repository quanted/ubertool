#Starting from python 2.7 base image
FROM python:2.7

#Set working directory to app to run commands
WORKDIR /app

#Add requirements file before install requirements
COPY requirements.txt ./requirements.txt

#Install requirements, including nose2
RUN pip install -r requirements.txt

#Add the whole repository to the container
COPY . ./

