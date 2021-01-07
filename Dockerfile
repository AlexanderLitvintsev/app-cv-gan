# set base image (host OS)
FROM python:3.8
# set the working directory in the container
WORKDIR /app
# install libraries for Linux
RUN apt-get update && \
    apt-get install libgl1-mesa-glx -y
# copy the dependencies file to the working directory
COPY requirements.txt .
# install dependencies
RUN pip install -r requirements.txt
# copy the content of the local directory to the working directory
COPY . ./app/
# command to run on container start
CMD [ "python", "./main.py" ]