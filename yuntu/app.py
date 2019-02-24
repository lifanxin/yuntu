# -*- coding: utf-8 -*-

from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, Response

from work import worker


app = Flask(__name__)

Bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show', methods=['GET'])
def show():
    print(request)
    keyword = request.args.get('keyword')
    print(keyword)
    status_tuple = worker.start(keyword)
    if not status_tuple:
        # fail to catch info
        name = 'code_503'
    elif status_tuple[0] == 'ok':
        name = status_tuple[1]
    return render_template('show.html', name=name)


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
