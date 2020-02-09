from flask import render_template, Flask, request, redirect
from Robot import Robot
import pandas as pd

app = Flask(__name__)

global robot


def index_sample():
    user = {'username': 'test'}
    return render_template('index.html', title='Home', user=user)


@app.route('/setup')
def setup():
    if robot.get_status() != 'ready':
        return redirect("index", code=303)
    return render_template('setup.html', title='Setup')


@app.route('/preparing')
def preparing():
    if robot.get_status() != 'resetting' and robot.get_status() != 'calculating':
        return redirect("/", code=303)
    return render_template('preparing.html', title='Preparing')


@app.route('/')
@app.route('/index')
def home():
    if robot.get_status() == 'ready':
        return redirect("setup", code=303)
    if robot.get_status() == 'resetting' or robot.get_status() == 'calculating':
        return redirect("preparing", code=303)
    return render_template('home.html', title='Setup')


@app.route('/state')
def test():
    return robot.get_state()


@app.route('/setup/submit', methods=['POST'])
def submit_params():
    if request.json is None:
        return {"error": "Request is not in JSON format"}
    if request.json.get("lat") is None or request.json.get("lon") is None or request.json.get("elevation") is None \
            or request.json.get("date") is None:
        return {"error": "Please fill out all the required fields"}
    if is_number(request.json.get("lat")) is False or is_number(request.json.get("lon")) is False:
        return {"error": "Latitude and longitude must be numbers"}
    if is_number(request.json.get("elevation")) is False:
        return {"error": "Elevation must be a number"}
    try:
        pd.to_datetime(request.json.get("date"), errors='raise')
    except ValueError:
        return {"error": "Invalid date: date must be in format MM/DD/YYYY"}

    robot.calculate(request.json.get("lat"), request.json.get("lon"),
                    request.json.get("elevation"), request.json.get("date"))
    return {"status": "success"}


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# start the webserver
if __name__ == "__main__":
    robot = Robot()
    app.debug = False
    app.run(use_reloader=False, threaded=True, host='0.0.0.0')
