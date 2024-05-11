import socket
import threading
import json
import datas.offline_data
import datas.setup_data
import handlers.login
import handlers.register

import handlers
import datas
import models
import models.community
import models.file


def handle_client(conn, addr):
    conn.settimeout(1)
    try:
        data = ""
        while True:
            try:
                data_1 = conn.recv(1024).decode('utf-8') 
                if not data_1:
                    break
                data += data_1 
                if data.endswith("\"}"):
                    print(data)
                    json_strings = data.split('}{')
                    for json_string in json_strings:
                        # 确保 JSON 字符串以 '{' 开头和 '}' 结尾
                        if not json_string.startswith('{'):
                            json_string = '{' + json_string
                        if not json_string.endswith('}'):
                            json_string += '}'
                        # 解析接收到的JSON数据
                        message = json.loads(json_string)
                        print(message)
                        if message["state"] == "100":
                            handlers.login.login(message,conn)
                        
                        elif message["state"] == "101":
                            handlers.register.register(message,conn)

                        elif message["state"] == '201':
                            datas.offline_data.out_offline_message(message,conn)
                        
                        elif message["state"] == "200":
                            models.community.community(message)

                        elif message["state"] == "301":
                            models.file.pre_store_file(message,conn)

                        elif message["state"] == "302":
                            models.file.store_file(message,conn)

                        elif message["state"] == "303":
                            models.file.finish_store_file()

                        elif message["state"] == "307":
                            models.file.send_offline_file_list(message,conn)

                        elif message["state"] == "306":
                            pass

                        elif message["state"] == "304":
                            print(125)
                            models.file.pre_send_file(message,conn)

                        elif message["state"] == "305":
                            print(111)
                            models.file.send_file(message,conn)
                        
                    data = ""
            except socket.timeout:
                continue
            except Exception as e:
                print(e)
                break
    except ConnectionAbortedError as e:
        # print(e)
        pass
    except ConnectionResetError as e:
        # print(e)
        pass
    # 客户端断开连接时,将其从在线用户中移除
    for account, connection in datas.setup_data.online_users.items():
        print(conn)
        print(connection)
        if connection == conn:
            print(account)
            del datas.setup_data.online_users[account]
            break
    
    conn.close()