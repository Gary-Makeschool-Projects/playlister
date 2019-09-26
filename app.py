import os
import sys


try:
    from flask import Flask, render_template, redirect, request
    import requests
except (ImportError, ModuleNotFoundError) as e:
    print(e, file=sys.stderr)
    print("run pipenv install 'moduleName' in your terminal ")


os.environ['FLASK_ENV'] = 'development'  # set flask envoirnment variable

app = Flask(__name__)
portnum = 8080  # custome port to run server on


@app.route('/')
@app.route('/index')
def index():
    """Return homepage."""
    render_template('home.html', msg='Hi my name is server')


if __name__ == '__main__':
    app.run(port=portnum)
