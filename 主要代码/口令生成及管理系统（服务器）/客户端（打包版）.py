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


if __name__ == '__main__':
    message = input(">>>")
    re=co(message)
    print(re)
#[{"time": "20170101070311", "amount": "3088", "productid": "45454455555", "productname": "iphone7"}, {"time": "20170101050311", "amount": "18", "productid": "453455772955", "productname": "xmz"}]

#注册命令  函数名：zhuce()
#[{"caozuoma": "0", "username": "llk", "s1": "0", "s2": "0","beizhu": "0", "passwd": "043633ea7324c9121a70990d8e2ed0d9ca1d417b5cf3c6222ebcd08f19252b007150e4787108f3a6ee26a8ef9a768d4f4c2bdbb4f032fefd91b1eeff6f70493c76d951802dde7933c9972e1bc0dff9c23b57eb8bc413e3a6ec54f40500d4cc80bfbd53785ca6e5b386a3a2"}]     #密码：D:zvl1h63K
#登录命令  函数名：denglu()
#[{"caozuoma": "1", "username": "llk", "s1": "0", "s2": "0","beizhu": "0", "passwd": "043633ea7324c9121a70990d8e2ed0d9ca1d417b5cf3c6222ebcd08f19252b007150e4787108f3a6ee26a8ef9a768d4f4c2bdbb4f032fefd91b1eeff6f70493c76d951802dde7933c9972e1bc0dff9c23b57eb8bc413e3a6ec54f40500d4cc80bfbd53785ca6e5b386a3a2"}]
#上传命令  函数名：shangchuan()
#[{"caozuoma": "2", "username": "llk", "s1": "0474ea90ca54002637181f5c79ee950ff541cef1367b9be2d03041fd982eea6beb816bb4823f36f2d6a3455f0fc407b8536a7e987cb5ee172faf009805e2f88ba0a5101063212548f5b4760ba17a0da55f6964d9e9ba0f018ca9c1c32ca7ab93846049d65e3b69280b9dbe15e6e75087ee68e2", "s2": "040211253b9e6c0aceb65a0d84e290acf4691c62cbf03edc03e3a53eaefd625e5c6fa2acd02160663ec5f6b8cf5d12cc8651f71eb3b43bab1785d7746dd5c34c8f23a9ce528a38a9f6770105113cd4df613b6c941af9e52de6be833997b336c42569b33a738b736ce4777b","beizhu": "qq", "passwd": "0"}]
#查询列表  函数名：xiazai1()
#[{"caozuoma": "3", "username": "llk", "s1": "0", "s2": "0","beizhu": "0", "passwd": "0"}]
#查询密码  函数名：xiazai2()
#[{"caozuoma": "4", "username": "llk", "s1": "0", "s2": "0","beizhu": "qq", "passwd": "0"}]
#删除     函数名：shanchu()
#[{"caozuoma": "5", "username": "llk", "s1": "0", "s2": "0", "beizhu": "qq", "passwd": "0"}]