import datas
import datas.setup_data
import json
def register(message,conn):
    if  datas.setup_data.is_setup(message):
        send = {"state":"403"}
        conn.send(json.dumps(send).encode())
    else:
        send = {"state":"402"}
        conn.send(json.dumps(send).encode())
        datas.setup_data.in_register_users(message)
