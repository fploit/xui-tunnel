from flask import Flask, request
from flask_cors import CORS
from tunnels import *


app = Flask(__name__)
CORS(app)


@app.route("/", methods=['POST', 'GET'])
def index():
    return 'Hello Baby.'


@app.route("/tunnel_list", methods=['POST'])
def tunnel_list():
    res = find_tunnel_list()
    return res


@app.route("/add_tunnel", methods=['POST'])
def tunnel_add():
    res = add_tunnel(
        request.json['ir_ip'],
        request.json['eu_ip'],
        request.json['start_point'],
        request.json['end_point'],
        request.json['remark']
    )
    return res


@app.route("/del_tunnel", methods=['POST'])
def tunnel_del():
    res = del_tunnel(
        request.json['point']
    )
    return res