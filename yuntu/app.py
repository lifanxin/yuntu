# -*- coding: utf-8 -*-

from os import path

from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, Response

from worker.leader import Leader


app = Flask(__name__)

Bootstrap = Bootstrap(app)
CURRENT_PATH = path.dirname(path.abspath(__file__))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show', methods=['GET'])
def show():
    print(request)
    user_input = request.args.get('keyword')

    leader = Leader()
    b64_str = leader.start(user_input)
    if not b64_str:
        # fail to catch info
        code = 'code_503'
    else:
        code = b64_str
    return render_template('show.html', name=code)


# send image by path
@app.route('/test/<string:name>')
def test(name):
    path = './work/data/{}.png'.format(name)
    with open(path, 'rb') as f:
        image = f.read()
    res = Response(image, mimetype="image/jpeg")
    return res


@app.route('/support')
def support():
    return render_template('support.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404
