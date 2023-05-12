# code by t.me/fploit
import json
import socket
import requests
import time
import uuid


def login(username, password, address):
    res = requests.post(
        url=f'http://{address}/login',
        json={
            "username": username,
            "password": password
        }
    )
    if res.json()['success'] == True:
        f = open(f'./sessions/{address}.txt', 'w')
        f.write(res.headers['Set-Cookie'])
        f.close()
        return "ok"
    else:
        return "error"



def list(address):
    session = 0
    try:
        session = open(f'./sessions/{address}.txt', 'r').read()
    except:
        data = json.loads(open('./servers.json', 'r').read())[address]
        log = login(data['username'], data['password'], address)
        session = open(f'./sessions/{address}.txt', 'r').read()
    res = requests.post(
        url=f'http://{address}/xui/inbound/list',
        headers={"cookie": session}
    )
    if res.status_code == 404:
        data = json.loads(open('./servers.json', 'r').read())[address]
        log = login(data['username'], data['password'], address)
        if log == "error":
            return "login error"
        session = open(f'./sessions/{address}.txt', 'r').read()
        res = requests.post(
            url=f'http://{address}/xui/inbound/list',
            headers={"cookie": session}
        )
        return res.json()
    else:
        return res.json()



def add(server_name, remark):
    data = json.loads(open('./servers.json', 'r').read())[server_name]
    address = data['eu']+":"+data['eu_port']
    log = login(data['username'], data['password'], address)
    if log == "error":
        return "login error"
    session = open(f'./sessions/{address}.txt', 'r').read()

    sock = socket.socket()
    sock.bind(('', 0))
    new_port = sock.getsockname()[1]

    ts = int(time.time()) * 1000 + 1000*60*60*24*30 #30 day

    random_id = str(uuid.uuid4())

    res = requests.post(
        url=f'http://{address}/xui/inbound/add',
        headers={"cookie": session},
        json={
            "up": 0,
            "down": 0,
            "total": 53687091200, #50GB
            "remark": remark,
            "enable": False,
            "expiryTime": ts,
            "listen": "",
            "port": new_port,
            "protocol": "vmess",
            "settings": '{"clients": [{"id": "'+ random_id +'","alterId": 0}],"disableInsecureEncryption": false}',
            "streamSettings": '{"network": "tcp","security": "none","tcpSettings": {"header": {"type": "none"}}}',
            "sniffing": '{"enabled": true,"destOverride": ["http","tls"]}'
        }
    )
    return {
        "server_res": res.json(),
        "port": new_port,
        "random_id": random_id,
        "time": ts
    }


def delete(address, id):
    session = 0
    try:
        session = open(f'./sessions/{address}.txt', 'r').read()
    except:
        data = json.loads(open('./servers.json', 'r').read())[address]
        log = login(data['username'], data['password'], address)
        session = open(f'./sessions/{address}.txt', 'r').read()
    res = requests.post(
        url=f'http://{address}/xui/inbound/del/{id}',
        headers={"cookie": session}
    )
    return res.json()




def find_tunnel_list(ip):
    api = f'http://{ip}:5000/tunnel_list'
    res  = requests.post(api).json()
    return res


def add_tunnel(ir_ip, eu_ip, start_point, end_point, remark):
    api = f'http://{ir_ip}:5000/add_tunnel'
    res  = requests.post(
        url=api,
        json={
            "ir_ip": ir_ip,
            "eu_ip": eu_ip,
            "start_point": start_point,
            "end_point": end_point,
            "remark": remark
        }
    )
    return res


def del_tunnel(ir_ip, eu_ip, point):
    api = f'http://{ir_ip}:5000/del_tunnel'
    res  = requests.post(
        url=api,
        json={
            "eu_ip": eu_ip,
            "point": point,
        }
    )
    return res




