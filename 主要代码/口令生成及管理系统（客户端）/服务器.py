import socket
import json
import pymysql
import jiemi

# 连接数据库，执行相关命令
def sqlexecute(sql):
    db = pymysql.connect(host='127.0.0.1',
                         user='root',
                         password='xjy014581',
                         database='test',
                         autocommit=True)

    cursor = db.cursor()  # 建立游标对象
    cursor.execute(sql)  # 执行sql命令
    # cursor.execute('select * from users;')
    ##print(result)
    result = cursor.fetchall()
    # print(result)
    cursor.close()  # 关闭游标对象
    db.close()  # 关闭数据库连接
    return result


# 处理服务器收到的指令
def handle_client_request(service_client_socket, ip_port):
    recv_data = service_client_socket.recv(1024)
    if recv_data:
        message = recv_data.decode()

        order = json.loads(message)
        print(message)
        print(order)
        # 根据操作码选择要进行的操作，调用相应函数
        # 操作码为0时，进行注册操作
        if order[0]["caozuoma"] == '0':
            zhuce(service_client_socket, ip_port, order)
        elif order[0]["caozuoma"] == '1':
            denglu(service_client_socket, ip_port, order)
        elif order[0]["caozuoma"] == '2':
            shangchuan(service_client_socket, ip_port, order)
        elif order[0]["caozuoma"] == '3':
            xiazai1(service_client_socket, ip_port, order)
        elif order[0]["caozuoma"] == '4':
            xiazai2(service_client_socket, ip_port, order)
        elif order[0]["caozuoma"] == '5':
            shanchu(service_client_socket, ip_port, order)
        # service_client_socket.send("已接收...".encode())
        service_client_socket.close()
    else:
        print("客户端下线了:", ip_port)
        print()

    service_client_socket.close()


# 注册：收到注册命令（操作码为0）时调用，完成添加users表信息，和建立用户的密码表两条sql命令
def zhuce(service_client_socket, ip_port, order):
    # order:[{"caozuoma(操作码)":"0(0（注册）/1（上传）/2（下载）/3（删除）)"，“username(用户名)”：“xmz”，“s1(密文1)”：“0（除了上传的时候，其余时候默认为0）”，“s2(密文2)”：“0（除了上传的时候，其余时候默认为0）”，“beizhu(备注)”：“0（默认为0）”，“passwd(注册密码)”：“123456”}]
    # [{"caozuoma":"0"，“username”：“xmz”，“s1”：“0”，“s2”：“0”，“beizhu”：“0”，“passwd”：“123456”}]

    # 执行第一条命令
    # insert into user(name,passwd) values('xmz','123456');
    a = "insert into users(name,passwd) values('"
    b = "','"
    c = "');"
    sql1 = a + order[0]['username'] + b + order[0]['passwd'] + c
    # 执行sql命令，对数据库进行操作：1.在user表中添加注册信息 2.在数据库中给注册用户创建一个空表
    sqlexecute(sql1)
    # print(sql1)

    # 执行第二条命令
    # create table xmz(id int auto_increment primary key not null,zhanghao varchar(260) not null,mima varchar(260) not null,beizhu varchar(100) not null unique);
    a1 = "create table "
    b1 = "(id int auto_increment primary key not null,zhanghao varchar(260) not null,mima varchar(260) not null,beizhu varchar(100) not null unique);"
    sql2 = a1 + order[0]['username'] + b1
    # print(sql2)
    sqlexecute(sql2)

    service_client_socket.send("0".encode())


# 解密函数用于登陆时验证口令
def de(s):
    m=jiemi.decry(s)
    return m


# 登录：收到登录命令（操作码为1）时调用，调用解密函数，对比密码是否相同，相同返回0，不同返回1

def denglu(service_client_socket, ip_port, order):
    # 登录命令 [{"caozuoma": "1", "username": "llk", "s1": "0", "s2": "0","beizhu": "0", "passwd": "123456"}]

    # 执行第一条命令
    # select passwd from users where name='xmz'
    a = "select passwd from users where name='"
    b = "'"
    sql1 = a + order[0]['username'] + b
    # 执行sql命令，对数据库进行操作：1.在user表中添加注册信息 2.在数据库中给注册用户创建一个空表
    result = sqlexecute(sql1)
    # print(result[0][0])
    # 如果解密后passwd和数据库中相同，返回‘0’表示登陆成功，否则返回‘1’表示登陆失败
    if de(result[0][0]) == de(order[0]['passwd']):
        service_client_socket.send("0".encode())
    else:
        service_client_socket.send("1".encode())


def shangchuan(service_client_socket, ip_port, order):
    # 上传命令  [{"caozuoma": "2", "username": "llk", "s1": "123456", "s2": "123456","beizhu": "qq", "passwd": "0"}]
    # insert into llk(zhanghao,mima,beizhu) values('123456','123456','qq');
    a = "insert into "
    b = "(zhanghao,mima,beizhu) values('"
    c = "','"
    d = "');"
    sql = a + order[0]['username'] + b + order[0]['s1'] + c + order[0]['s2'] + c + order[0]['beizhu'] + d
    result = sqlexecute(sql)
    print(result)
    service_client_socket.send("0".encode())



def xiazai1(service_client_socket, ip_port, order):
    #[{"caozuoma": "3", "username": "llk", "s1": "0", "s2": "0", "beizhu": "0", "passwd": "0"}]
    #select beizu from llk;
    sql="select beizhu from "+order[0]['username']+";"
    result = sqlexecute(sql)
    print(result)
   #socket.send函数不能传输元组，用json.dumps()函数变成json字符串，在客户端要记得用json.loads()函数
    me=json.dumps(result)
    service_client_socket.send(me.encode())

def xiazai2(service_client_socket, ip_port, order):
    #[{"caozuoma": "4", "username": "llk", "s1": "0", "s2": "0", "beizhu": "qq", "passwd": "0"}]
    #select zhanghao,mima from llk where beizhu='qq';
    sql="select zhanghao,mima from "+order[0]['username']+ " where beizhu='"+order[0]['beizhu']+"';"
    #print(sql)
    result = sqlexecute(sql)#执行sql命令
    print(result)
    # socket.send函数不能传输元组，用json.dumps()函数变成json字符串，在客户端要记得用json.loads()函数
    me = json.dumps(result)
    service_client_socket.send(me.encode())


#调用shanchu（）之前应该先调用xiazai1（）给用户返回可删除的列表
def shanchu(service_client_socket, ip_port, order):
    # [{"caozuoma": "5", "username": "llk", "s1": "0", "s2": "0", "beizhu": "qq", "passwd": "0"}]
    # delete from llk where beizhu='qq';
    sql="delete from "+order[0]['username']+" where beizhu='"+order[0]['beizhu']+"';"
    #print(sql)
    result = sqlexecute(sql)  # 执行sql命令
    #print(result)
    service_client_socket.send("0".encode())



if __name__ == '__main__':
    # 创建tcp服务端套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口复用，让程序退出后端口号立即释放
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定IP与端口号
    tcp_server_socket.bind(("192.168.93.150", 9090))
    # 设置监听
    tcp_server_socket.listen(128)
    print('服务器已经开始运行')
    # 循环等待接受客户端连接请求
    while True:
        # 等待接收客户端连接请求
        service_client_socket, ip_port = tcp_server_socket.accept()
        print("客户端连接成功:", ip_port)
        handle_client_request(service_client_socket, ip_port)  # 分析json格式的命令，决定调用某操作（注册，上传，登录等）的函数