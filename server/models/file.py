import os
import json
open_file_name = []


def pre_store_file(message,conn):
    name = message["data"].split(":")[0]
    if not os.path.isdir("datas/files/{}".format(message["receiver"])):
        try:
            os.mkdir("datas/files/{}".format(message["receiver"]))
        except Exception as e:
            print(e)
    if not os.path.isfile("datas/files/{}/{}_{}".format(message["receiver"],message["sender"],name)):
        try:
           with open("datas/files/{}/{}_{}".format(message["receiver"],message["sender"],name), "w") as file: 
               send = {"state":"421","data":"0"}
               conn.send(json.dumps(send).encode())
        except Exception as e:
            
            print("预接收文件异常：",e)
    else:
        try:
            number = os.path.getsize("datas/files/{}/{}_{}".format(message["receiver"],message["sender"],name))
            send = {"state":"421","data":number}
            conn.send(json.dumps(send).encode())
        except Exception as e:
            print("预接收文件异常：",e)
    open_file_name.append(name)

def store_file(message,conn):
    name = open_file_name.pop()
    with open("datas/files/{}/{}_{}".format(message["receiver"],message["sender"],name), "a",encoding='utf-8') as file:
        file.write(message["data"])
        file.close()
    open_file_name.append(name)
    with open("datas/files/{}/{}_{}".format(message["receiver"],message["sender"],name), "r",encoding='utf-8') as file:
        a = file.read()
        num = len(a)
        file.close()
    send = {"state":"421","receiver":message["sender"],"data":num}
    conn.send(json.dumps(send).encode('utf-8'))

def finish_store_file():
    open_file_name.pop()

def send_offline_file_list(message,conn):
    send_name = ""
    name_list = []
    if os.path.isdir("datas/files/{}".format(message["sender"])):
        list = os.listdir("datas/files/{}".format(message["sender"]))
        for each_file in list:
            file_name = each_file.split('_')
            send_name = file_name[0] + ':' + file_name[1]
            name_list.append(send_name)
            send_name = ""
        send = {"state":"407","receiver":message["sender"],"data":name_list}
        conn.send(json.dumps(send).encode('utf-8'))
    else:
        send = {"state":"408","receiver":message["sender"]}
        conn.send(json.dumps(send).encode('utf-8'))


def pre_send_file(message,conn):
    if os.path.isdir("datas/files/{}".format(message["sender"])):
        list = os.listdir("datas/files/{}".format(message["sender"]))
        flag = 1
        for file_name in list:
            name = file_name.split('_')
            if name[1] == message["data"]:
                 with open("datas/files/{}/{}".format(message["sender"],file_name), "r",encoding='utf-8') as file:
                    a = file.read()
                    num = len(a)
                    send = {"state":"423","sender":name[0],"receiver":message["sender"],"data":f"{file_name}:{num}"}
                    flag = 0
                    file.close()
        if flag:
            send = {"state":"422"}
    else:
        send = {"state":"422"}
    conn.send(json.dumps(send).encode('utf-8'))

def send_file(message,conn):
    file_name = message["data"].split(':')
    name = file_name[0]
    num = int(file_name[1])
    if os.path.isdir("datas/files/{}".format(message["sender"])):
        list = os.listdir("datas/files/{}".format(message["sender"]))
        for file_name_1 in list:
            name_1 = file_name_1.split('_')
            if file_name_1 == name:
                with open("datas/files/{}/{}".format(message["sender"],file_name_1), "r", encoding='utf-8') as file:
                    b = file.read()
                    file_size = len(b)
                    file.close()
                if num >= file_size:
                    send ={"state":"425"}
                    conn.send(json.dumps(send).encode('utf-8'))
                elif num < file_size:
                    with open("datas/files/{}/{}".format(message["sender"],file_name_1), "r", encoding='utf-8') as file:
                        file.read(num)
                        data = file.read(1024)
                        send = {"state":"424","sender":name_1[0],"receiver":message["sender"],"data":data}
                        conn.send(json.dumps(send).encode('utf-8'))
                        file.close()
                    break

                 
