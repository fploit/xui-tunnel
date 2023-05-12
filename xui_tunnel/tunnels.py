#code by t.me/fploit
import os


def find_tunnel_list():
    payload = "ps aux | grep '[s]sh.*-f'"
    res = os.popen(payload).read().splitlines()
    return res


def add_tunnel(ir_ip, eu_ip, start_point, end_point, remark):
    payload = f'ssh -f -N root@{eu_ip} -L {ir_ip}:{start_point}:{eu_ip}:{end_point} "{remark}"'
    os.system(payload)
    return "ok"


def del_tunnel(point):
    points = find_tunnel_list()
    for tunnel in points:
        scope = tunnel.split(" ")
        scope = list(filter(("").__ne__, scope))
        port = scope[len(scope) - 1].split(":")[3]
        if str(point) == port:
            pid = scope[1]
            print(pid)
            os.system(f'kill {pid}')
   
    return "ok"


