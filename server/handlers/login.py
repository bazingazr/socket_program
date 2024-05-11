import datas
import datas.setup_data
import json

def login(message,conn):
    if datas.setup_data.is_setup(message):
        send = {"state":"400"}
        conn.send(json.dumps(send).encode())
        datas.setup_data.in_online_users(message,conn)
    else:
        send ={"state":"401"}
        conn.send(json.dumps(send).encode())
