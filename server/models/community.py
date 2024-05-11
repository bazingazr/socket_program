import datas
import datas.offline_data
import datas.setup_data
import json
def community(message):
    if datas.setup_data.is_online(message):
        send = message
        send["state"] = '406'
        conn = datas.setup_data.online_users[message["receiver"]]
        conn.send(json.dumps(send).encode())
    else:
        datas.offline_data.in_offline_message(message)

def send(message,conn):
    conn.send(json.dumps(message).encode())
