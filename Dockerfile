#Starting from ubuntu base image
FROM ubuntu:14.04
RUN apt-get update

#Installing python, pip
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN apt-get clean all

#Set working directory to app to run commands
WORKDIR /app

#Add requirements file before install requirements
COPY requirements.txt ./requirements.txt

#Install requirements, including nose2
RUN pip install -r requirements.txt

#Add the whole repository to the container
COPY . ./
