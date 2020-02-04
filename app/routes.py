from flask import render_template, Flask, request

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'test'}
    print(test)
    return render_template('index.html', title='Home', user=user)

@app.route('/setup')
def setup():
    return render_template('setup.html', title='Setup')

# start the webserver
if __name__ == "__main__":
    print("initiated")
    test = "hello"
    app.debug = True
    app.run()