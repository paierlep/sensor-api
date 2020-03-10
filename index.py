from flask import Flask, request, jsonify
import sqlite3
import time
import os
import sys

database_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "database.db")

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_api_version():
    return 'API V1'

@app.route('/api/get/all', methods=['GET', 'OPTIONS'])
def get_all_data():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
    try:
      with sqlite3.connect(database_dir) as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM sensor_measurements")
        return _corsify_actual_response(jsonify(cur.fetchall()))
    except Exception as exception:
        print(exception,  file=sys.stderr)
        db.rollback()
    finally:
        db.close()
    return 'OK'

@app.route('/api/get/latest', methods=['GET', 'OPTIONS'])
def get_latest_data():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
    try:
      with sqlite3.connect(database_dir) as db:
        cur = db.cursor()
        cur.execute(("SELECT sm.* from sensor_measurements sm inner join "
                     "(select sensor, max(timestamp) as maxdate from sensor_measurements group by sensor) t "
                     "on t.sensor=sm.sensor and t.maxdate=sm.timestamp"))
        return _corsify_actual_response(jsonify(cur.fetchall()))
    except Exception as exception:
        print(exception,  file=sys.stderr)
        db.rollback()
    finally:
        db.close()
    return 'OK'

@app.route('/api', methods=['POST'])
def store_data():
    data = request.get_json()
    try:
      with sqlite3.connect(database_dir) as db:
        cur = db.cursor()
        cur.execute("INSERT INTO sensor_measurements"
                    "(timestamp, sensor, humidity, temperature, pressure)"
                    "VALUES(?,?,?,?,?)",
                    (int(time.time()),
                     data.get("sensor"),
                     data.get("humidity"),
                     data.get("temperature"),
                     data.get("pressure")
                    )
                   )
        db.commit()
    except Exception as exception:
        print(exception,  file=sys.stderr)
        db.rollback()
    finally:
        db.close()
    return 'OK'

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
