# TODO: CHANGE LOGIN METHOD TO USERNAME & PASSWORD
import json
import os

from flask import Flask, session, render_template, send_from_directory, request

import dropbox_service

app = Flask(__name__)

TOKEN = ''
with open('token.txt', 'r')as f:
    global TOKEN
    TOKEN = f.read()

dbx = dropbox_service.DropboxService(token=TOKEN)


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
    return json.dumps(dbx.read())  # return as JSON compatible string


# write
@app.route('/crud/write', methods=['POST'])
def write():
    return dbx.write(request.form['filename'], request.form['data'])


# delete
@app.route('/crud/delete', methods=['DELETE'])
def delete():
    value = dbx.delete(request.headers.get('filename'))
    return str(value), value


# error handler for 404
@app.errorhandler(404)
def error(e):
    return render_template('error.html', status=e.code), e.code


# route urls for static files
@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run()
