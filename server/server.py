import datas.setup_data
import handlers.handle
import utils
import handlers
import models
import socket
import threading
import json
import datas
thread_flag = 0
def is_set():
    if thread_flag:
        return True
    else:
        return False

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8888))
    server_socket.listen(5)
    server_socket.settimeout(1)  # 设置 1 秒超时
    while not is_set():
        try:
            client_socket,client_addr = server_socket.accept()
            print(f"客户端 {client_addr} 已连接")
            client_thread = threading.Thread(target=handlers.handle.handle_client, args=(client_socket, client_addr))
            client_thread.start()
        except socket.timeout:
            continue
if __name__ == "__main__":
    min_thread = threading.Thread(target=start_server, args=())
    min_thread.start()
    try:
        while True:
            pass
    except(KeyboardInterrupt):
        thread_flag = 1

    