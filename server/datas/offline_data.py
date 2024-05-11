import json
# 存储离线消息
offline_messasge = {}

# 离线消息存储函数
def in_offline_message(message):
    if message["receiver"] not in offline_messasge:
        offline_messasge[message["receiver"]] = {}
    if message["sender"] not in offline_messasge[message["receiver"]]:
        offline_messasge[message["receiver"]][message["sender"]] = []
    offline_messasge[message["receiver"]][message["sender"]].append(message["data"])

# 离线消息释放函数
def out_offline_message(message,conn):
    print(offline_messasge)
    if message["sender"] in offline_messasge:
        for sender,info in (offline_messasge[message["sender"]]).items():
            send = {"state" : "405"}
            send["sender"] = sender
            send["receiver"] = message["sender"]
            for infomation in info:
                send["data"] = infomation
                conn.send(json.dumps(send).encode())
        del offline_messasge[message["sender"]]
        send = {"state":"407"}
        conn.send(json.dumps(send).encode())
    else:
        send = {"state":"404"}
        conn.send(json.dumps(send).encode())


    
