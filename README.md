# Sensors backend

Provides a basic backend for sensor

## Installation

Start a virtualenv and install all the requirements:

```
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

## Usage

Start a development server with

```
FLASK_APP=index.py flask run --host=0.0.0.0
```

for productional please refer to:
https://flask.palletsprojects.com/en/1.1.x/deploying/

## Description

Currently there are three API endpoints provided

- [POST] /api to store the measurement data
  a sample json might look like:
  ```
  {
    "name": "some sensor name",
    "humidity": "40.5",
    "temperature": "27.5",
    "pressure": "1000.0"
  }
  ```

- [GET, OPTIONS] /api/get to fetch the metadata
  currently the complete database output is delivered as a json data

- [GET, OPTIONS] /api/get/latest to fetch the most current data for each room separately
