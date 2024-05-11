import socket
import threading
import json

# 存储注册用户的账号和密码
registered_users = {}
# 存储在线用户的连接和账号
online_users = {}
offline_messages = {}
def handle_client(conn, addr):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            # 解析接收到的JSON数据
            message = json.loads(data)

            if message["type"] == "login":
                account = message["account"]
                password = message["password"]

                if account in registered_users and registered_users[account] == password:
                    online_users[account] = conn
                    response = {"type": "login", "success": True}
                else:
                    response = {"type": "login", "success": False}

                conn.send(json.dumps(response).encode())

            elif message["type"] == "register":
                account = message["account"]
                password = message["password"]

                if account not in registered_users:
                    registered_users[account] = password
                    response = {"type": "register", "success": True}
                else:
                    response = {"type": "register", "success": False}

                conn.send(json.dumps(response).encode())

            elif message["type"] == "message":
                sender = message["sender"]
                recipient = message["recipient"]
                content = message["content"]

                if recipient in online_users:
                    response = {"type": "message", "sender": sender, "content": content}
                    online_users[recipient].send(json.dumps(response).encode())







        except ConnectionResetError:
            break

    # 客户端断开连接时,将其从在线用户中移除
    for account, connection in online_users.items():
        if connection == conn:
            del online_users[account]
            break

    conn.close()

def store_offline_message(self, receiver_socket, message):
        # 如果接收者不在线，存储离线消息
    if receiver_socket not in online_users:
        if receiver_socket not in offline_messages:
            offline_messages[receiver_socket] = []
        offline_messages[receiver_socket].append(message)

def send_offline_messages(self, client_socket):
            # 检查该客户端是否有离线消息
    if client_socket in offline_messages:
        for offline_message in offline_messages[client_socket]:
                    client_socket.send(offline_message.encode())
        del offline_messages[client_socket]
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8888))
    server_socket.listen(5)

    print("服务器已启动,等待客户端连接...")

    while True:
        conn, addr = server_socket.accept()
        print(f"客户端 {addr} 已连接")

        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()


if __name__ == "__main__":
    start_server()