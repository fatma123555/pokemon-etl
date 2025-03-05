# setup docker image with python
FROM python:3.11

# move requirements txt file to a folder within the container and install requirements
COPY requirements.txt ./config/credential.json ./config/config_file.json /tmp/
RUN pip install --requirement /tmp/requirements.txt

# add python app file to docker
ADD app.py .

# run python app command
CMD ["python", "./app.py"]

