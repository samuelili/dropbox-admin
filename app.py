import logging
import os
import yaml
from flask import json
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session

import dropbox_service
from flask import Flask

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

app.secret_key = os.urandom(24)

service = None


def start():
    global service
    try:
        with open('token.yaml', 'r') as token_file:
            config = yaml.load(token_file)
            service = dropbox_service.DropboxService(token=config['dropbox-token'])
            app.run()
    except IOError:
        logging.error("Error reading token.yaml. Please make sure the token.yaml file is properly configured.")


# root page
@app.route('/')
def index():
    return render_template('index.html')


# login page
@app.route('/login')
def login():
    return render_template('login.html'), 302


# save token
@app.route('/crud/token', methods=['POST'])
def save_token():
    session['token'] = request.form['token']
    return "201", 201


# read
@app.route('/crud/read', methods=['GET'])
def read():
    return json.dumps(service.read())  # return as JSON compatible string


# write
@app.route('/crud/write', methods=['POST'])
def write():
    return service.write(request.form['filename'], request.form['data'])


# delete
@app.route('/crud/delete', methods=['DELETE'])
def delete():
    value = service.delete(request.headers.get('filename'))
    return str(value), value


# error handler for 404
@app.errorhandler(404)
def error(e):
    return render_template('error.html', status=e.code), e.code


# route urls for static files
@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('static', path)
