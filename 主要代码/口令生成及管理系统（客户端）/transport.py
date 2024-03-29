import socket  # 导入 socket 模块
import json



def co(message):
    sk = socket.socket()  # 创建 socket 对象

    port = 9090  # 设置端口号

    sk.connect(('192.168.93.150', port))  # 连接服务器
    try:
        # message = input(">>>")
        sk.send(message.encode())  # 发送json格式的命令
    except KeyboardInterrupt:
        print("x")
    re=(sk.recv(1024).decode())
    sk.close()
    return re
