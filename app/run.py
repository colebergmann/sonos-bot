from flask import render_template, Flask, request
from Robot import Robot
import pandas as pd

app = Flask(__name__)

global robot


def index_sample():
    user = {'username': 'test'}
    return render_template('index.html', title='Home', user=user)


@app.route('/setup')
def setup():
    return render_template('setup.html', title='Setup')


@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html', title='Setup')


@app.route('/state')
def test():
    return robot.get_state()


@app.route('/setup/submit', methods=['POST'])
def submit_params():
    if request.json["lat"] is None or request.json["long"] is None or request.json["elevation"] is None \
            or request.json["date"] is None:
        return {"error": "Please fill out all the required fields"}
    if is_number(request.json["lat"]) is False or is_number(request.json["long"]) is False:
        return {"error": "Latitude and longitude must be numbers"}
    if is_number(request.json["elevation"]) is False:
        return {"error": "Elevation must be a number"}
    try:
        pd.to_datetime(request.json["date"], errors='raise')
    except ValueError:
        return {"error": "Invalid date: date must be in format MM/DD/YYYY"}

    # if we got here, then all the inputs were valid
    # kick off the program and return a success message
    return {"status":"success"}


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# start the webserver
if __name__ == "__main__":
    robot = Robot()
    app.debug = True
    app.run(use_reloader=False, host='0.0.0.0')
