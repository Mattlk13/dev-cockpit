import os
from flask import Flask


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])


@app.route('/')
def hello():
    return "BIBBOX Developers Cockpit"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()