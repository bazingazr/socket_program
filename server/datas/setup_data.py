# 存储注册用户的账号和密码
registered_users = {"1234567890":"0"}

# 存储在线用户的连接和账号
online_users = {}


def is_setup(message):
    if message["sender"] in registered_users and message["data"] == registered_users[message["sender"]]:
        return True
    else:
        return False

def is_online(message):
    if message["receiver"] in online_users:
        return True
    else:
        return False

def in_online_users(message,conn):
    online_users[message["sender"]] = conn

def in_register_users(message):
    registered_users[message["sender"]] = message["data"]