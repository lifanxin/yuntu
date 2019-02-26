# -*- coding: utf-8 -*-

from os import path

from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, Response

from work import worker


app = Flask(__name__)

Bootstrap = Bootstrap(app)
CURRENT_PATH = path.dirname(path.abspath(__file__))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show', methods=['GET'])
def show():
    print(request)
    keyword = request.args.get('keyword')
    print(keyword)
    str = worker.start(keyword)
    if not str:
        # fail to catch info
        name = 'code_503'
    else:
        name = str
        # test
        # img_path = path.join(CURRENT_PATH, 'work/code.txt')
        # with open(img_path, 'r') as f:
        #     name = f.read()
    return render_template('show.html', name=name)


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
