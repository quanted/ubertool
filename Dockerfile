FROM puruckertom/uber_py27

#Set working directory to app to run commands
WORKDIR /app

#Add the whole repository to the container
COPY . ./
