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

application = Flask(__name__)

application.secret_key = os.urandom(24)

try:
    with open('token.yaml', 'r') as token_file:
        config = yaml.load(token_file)
    with open('pages.json', 'r') as f:
        pagesJson = jsonpickle.decode(f.read())
    service = dropbox_service.DropboxService(token=config['dropbox-token'])

except IOError:
    logging.error("Error reading token.yaml. Please make sure the token.yaml file is properly configured.")


# define contextual processes.
@application.context_processor
def pages_json():
    return dict(pages=pagesJson)


@application.route('/')
def index():
    return render_template('index.html', pages=pagesJson)


# shared link page
@application.route('/pages/links.html')
def link_page():
    return render_template('links.html', pages=pagesJson)


@application.route('/links', methods=['GET'])
def list_all_shared_folders():
    force_update = (request.args.get('force-update') == "1")
    result = service.list_all_shared_folders(force_update=force_update)
    return json.dumps(json.loads(jsonpickle.encode(result)), indent=2)


@application.route('/members', methods=['GET'])
def list_all_team_members():
    return json.dumps(json.loads(jsonpickle.encode(service.list_team_members())), indent=2)


@application.route('/members/<team_member_id>/shared-folders', methods=['GET'])
def list_shared_folders(team_member_id):
    return json.dumps(json.loads(jsonpickle.encode(service.list_shared_folders(team_member_id))), indent=2)


@application.route('/members/<team_member_id>/shared-links', methods=['GET'])
def list_shared_links(team_member_id):
    return json.dumps(json.loads(jsonpickle.encode(service.list_shared_links(team_member_id))), indent=2)




'''

To be used in the future.


'''


# login page
@application.route('/login')
def login():
    return render_template('login.html'), 302


# read
@application.route('/items', methods=['GET'])
def read():
    return json.dumps(service.list_all())


@application.route('/progress', methods=['GET'])
def get_progress():
    return json.dumps(json.loads(jsonpickle.encode(service.progress)), indent=2)


@application.route('/test', methods=['GET'])
def list_all_groups():
    result = service.test()
    return json.dumps(json.loads(jsonpickle.encode(result)), indent=2)


@application.route('/crud/write', methods=['POST'])
def write():
    return service.write(request.form['filename'], request.form['data'])


@application.route('/crud/delete', methods=['DELETE'])
def delete():
    value = service.delete(request.headers.get('filename'))
    return str(value), value


@application.errorhandler(404)
def error(e):
    return render_template('error.html', status=e.code), e.code


@application.route('/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
