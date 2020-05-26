from flask import render_template, Flask, request, redirect, session
from Robot import Robot
import pandas as pd
from threading import Thread

app = Flask(__name__)

global robot


def index_sample():
    user = {'username': 'test'}
    return render_template('index.html', title='Home', user=user)


@app.route('/setup')
def setup():
    if not session.get('logged_in'):
        return render_template('login.html')
    if robot.get_status() != 'ready':
        return redirect("/", code=303)
    return render_template('setup.html', title='Setup')

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password':
        session['logged_in'] = True
    else:
        pass
    return redirect("/", code=303)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route('/preparing')
def preparing():
    if not session.get('logged_in'):
        return render_template('login.html')
    if robot.get_status() != 'resetting' and robot.get_status() != 'calculating':
        return redirect("/", code=303)
    return render_template('preparing.html', title='Preparing')


@app.route('/')
@app.route('/index')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    if robot.get_status() == 'ready':
        return redirect("setup", code=303)
    if robot.get_status() == 'resetting' or robot.get_status() == 'calculating':
        return redirect("preparing", code=303)
    return render_template('home.html', title='Setup')


@app.route('/state')
def state():
    return robot.get_state()

@app.route('/graph/azimuth')
def getAzimuthGraph():
    return robot.get_azimuth_graph()

@app.route('/graph/elevation')
def getElevationGraph():
    return robot.get_elevation_graph()

@app.route('/graph/dni')
def getDniGraph():
    arr  = robot.get_dni_graph()
    print(arr)
    return arr

@app.route('/graph/temperature')
def getTemperatureGraph():
    return robot.get_temperature_graph()

@app.route('/setstatus/<string:s>', methods=["POST"])
def setState(s):
    if s == "pause":
        robot.pause()
    elif s == "resume":
        robot.resume()
    elif s == "cancel":
        robot.cancel()
        robot.__init__()
    else:
        return {"error": "Unknown state"}
    return {"status":"success"}


@app.route('/setup/submit', methods=['POST'])
def submit_params():
    if robot.get_status() != "ready":
        return {"error": "Robot is currently running a test. See the status <a href='/'>here</a>"}
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

    # start the calculations in a separate thread so we aren't clogging up the main thread
    Thread(target=robot.calculate, args=[float(request.json.get("lat")), float(request.json.get("lon")),
                                         float(request.json.get("elevation")), request.json.get("date"),
                                         request.json.get("speaker_color")]).start()
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
    app.debug = True
    app.secret_key = 'KMergmkerg8ergmklzmagnja8rg8rgnamgr'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(use_reloader=False, host='0.0.0.0')
