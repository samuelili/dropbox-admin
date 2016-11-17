import logging
import os

import jsonpickle as jsonpickle
import yaml
from flask import Flask
from flask import json
from flask import render_template
from flask import request
from flask import send_from_directory

import dropbox_service

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

app.secret_key = os.urandom(24)

with open('token.yaml', 'r') as token_file:
    config = yaml.load(token_file)

service = dropbox_service.DropboxService(token=config['dropbox-token'])

with open('pages.json', 'r') as f:
    pagesJson = jsonpickle.decode(f.read())


def start():
    global service
    try:
        app.run(debug=True)
    except IOError:
        logging.error("Error reading token.yaml. Please make sure the token.yaml file is properly configured.")


# define contextual processes.
@app.context_processor
def pages_json():
    return dict(pages=pagesJson)


# root page
@app.route('/')
def index():
    return render_template('index.html', pages=pagesJson)


# shared link page
@app.route('/pages/links.html')
def link_page():
    return render_template('links.html', pages=pagesJson)

# login page
@app.route('/login')
def login():
    return render_template('login.html'), 302


# read
@app.route('/items', methods=['GET'])
def read():
    return json.dumps(service.list_all())


@app.route('/links', methods=['GET'])
def list_all_shared():
    result = service.list_all_shared_folders()
    return json.dumps(json.loads(jsonpickle.encode(result)), indent=2)


@app.route('/crud/write', methods=['POST'])
def write():
    return service.write(request.form['filename'], request.form['data'])


@app.route('/crud/delete', methods=['DELETE'])
def delete():
    value = service.delete(request.headers.get('filename'))
    return str(value), value


@app.errorhandler(404)
def error(e):
    return render_template('error.html', status=e.code), e.code


@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('static', path)
