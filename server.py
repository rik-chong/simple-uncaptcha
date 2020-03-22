#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import flask
import subprocess
import os
from aip import AipOcr
from hashlib import md5
import time


def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


app = flask.Flask(__name__)
app.after_request(after_request)
API_KEY = os.getenv('AIP_API_KEY')
APP_ID = os.getenv('AIP_API_ID')
SECRET_KEY = os.getenv('AIP_SECRET_KEY')


@app.route('/x', methods=['POST'])
def query_captcha():
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    try:
        f = flask.request.files['file']
        tmp_filename = 'captcha-' + md5(str(time.time()).encode('utf8')).hexdigest()
        f.save(tmp_filename)
        image = None
        with open(tmp_filename, 'rb') as fp:
            image = fp.read()
            fp.close()
        options = {"recognize_granularity": "big", "detect_direction": "false"}
        result = client.numbers(image, options);
        os.remove(tmp_filename)
        return flask.Response(json.dumps({'code': 0, 'msg': '', 'result': result['words_result'][0]['words']}),
                              mimetype='application/json')
    except Exception as e:
        return flask.Response(json.dumps({'code': -1, 'msg': str(e), 'result': False}),
                              mimetype='application/json')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, threaded=True)
