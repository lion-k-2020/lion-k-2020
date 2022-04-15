import json

from flask import Response
from wxcloudrun.myEncoder import AlchemyEncoder, new_alchemy_encoder


def make_succ_empty_response():
    data = json.dumps({'code': 0, 'data': {}})
    return Response(data, mimetype='application/json')


def make_succ_response(data):
#     data = json.dumps({'code': 0, 'data': data}, cls=new_alchemy_encoder(), ensure_ascii=False)
    data = json.dumps({'code': 0, 'data': data}, ensure_ascii=False)
    return Response(data, mimetype='application/json')


def make_err_response(err_msg):
    data = json.dumps({'code': -1, 'errorMsg': err_msg})
    return Response(data, mimetype='application/json')
