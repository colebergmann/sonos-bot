from flask import render_template, Flask, request
from Robot import Robot

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
    if (request.args.get("lat") == None || request.args.get("long") == None
    return request.args


# start the webserver
if __name__ == "__main__":
    robot = Robot()
    app.debug = True
    app.run(use_reloader=False)