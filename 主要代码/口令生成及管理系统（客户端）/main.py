from PySide6.QtWidgets import QApplication, QLineEdit, QMessageBox,QPushButton,QLabel
from PySide6.QtGui import QIcon,QPixmap
from PySide6.QtUiTools import QUiLoader
import sys
import sm2,enjosn,pingce,transport
import global_variable as glv





class LogAndReg:
    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('loginAndregist.ui')
        #获取QstackWidget中的两个界面
        self.ui1 =self.ui.stackedWidget.widget(0)
        self.ui2 =self.ui.stackedWidget.widget(1)
        # 获取QStackedWidget中的当前页面，当前页面是登录界面
        current_page = self.ui.stackedWidget.currentWidget()
        # 获取登录页面中的所有组件
        self.login_pushButton=self.ui1.findChild(QPushButton, "login_pushButton")
        self.exit_pushButton=self.ui1.findChild(QPushButton, "exit_pushButton")
        self.username=self.ui1.findChild(QLineEdit, "username")
        self.password=self.ui1.findChild(QLineEdit, "password")
        self.regist_btn=self.ui1.findChild(QPushButton, "commandLinkButton")
        self.hideorshow_btn=self.ui1.findChild(QPushButton, "hideorshow_btn")
        #隐藏密码
        self.password.setEchoMode(QLineEdit.Password)

        #登录界面和注册界面的背景设置

        background_label = QLabel(self.ui)
        # 加载背景图片
        background_image = QPixmap("icon/background.png")
        # 设置背景图片到QLabel上
        background_label.setPixmap(background_image)
        # 调整QLabel的大小以适应窗口
        background_label.setGeometry(0, 0, self.ui.width(), self.ui.height())
        background_label.lower()
        #文本框变圆角
        my_line_edit = self.ui1.findChild(QLineEdit, "password")  # 替换为您的对象名称
        my_line_edit.setStyleSheet("border-radius: 10px;")
        my_line_edit1 = self.ui1.findChild(QLineEdit, "username")  # 替换为您的对象名称
        my_line_edit1.setStyleSheet("border-radius: 10px;")

        # 添加登录界面的信号和槽。
        self.exit_pushButton.clicked.connect(self.ui.close)
        self.login_pushButton.clicked.connect(self.log)
        self.regist_btn.clicked.connect(self.changeToRegist)
        self.hideorshow_btn.clicked.connect(self.hideOrShow)
        #登录界面的变量
        self.logpwdindex=0



        #获取注册页面中的所有组件
        self.UserName=self.ui2.findChild(QLineEdit, "UserName")
        self.PassWord=self.ui2.findChild(QLineEdit, "PassWord")
        self.PassWordSure=self.ui2.findChild(QLineEdit, "PassWordSure")
        self.ConfirmButton = self.ui2.findChild(QPushButton, "ConfirmButton")
        self.CancelButton =self.ui2.findChild(QPushButton, "CancelButton")
        self.RegPwd_hors_btn=self.ui2.findChild(QPushButton, "RegPwd_hors_btn")
        self.Pwdsure_hors_btn=self.ui2.findChild(QPushButton, "Pwdsure_hors_btn")
        # 添加注册界面的信号和槽。
        self.UserName.textChanged.connect(self.emit_Username)  # 姓名改变时
        self.PassWord.textChanged.connect(self.emit_Password)  # 密码
        self.PassWordSure.textChanged.connect(self.emit_ConPassword)  # 确认密码
        self.ConfirmButton.clicked.connect(self.emit_Confir_Button)  # 确认
        self.CancelButton.clicked.connect(self.changToLogin)
        self.RegPwd_hors_btn.clicked.connect(self.RegPwdhideOrShow)
        self.Pwdsure_hors_btn.clicked.connect(self.PwdsurehideOrShow)

        # 密码隐藏
        self.PassWord.setEchoMode(QLineEdit.Password)
        self.PassWordSure.setEchoMode(QLineEdit.Password)
        #注册界面的变量
        self.registindepwd=0
        self.registindexpwdsure=0
        #设置当前界面为登录界面
        self.ui.stackedWidget.setCurrentWidget(self.ui1)

        #在这个界面里实现一个查询界面的实例实现跳转
#登录界面中注册按钮的函数
    def changeToRegist(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui2)
# 登录的函数
    def log(self):
        if self.username.text().strip() == '' or self.password.text().strip() == '' :
            try:
                QMessageBox.information(self.ui, "error", "输入有误，请重新输入")
            except Exception as str:
                print("输入错误 %s" % (str))
        elif len(self.password.text()) < 6:
            QMessageBox.information(self.ui, "warning", "密码小于6位")
        else:
            self.M_UserName = self.username.text()
            self.M_PassWord = self.password.text()
            #将username设为全局变量方便在下一模块的使用
            glv._init()
            glv.set('username',self.M_UserName)

            # 加密
            #self.C_UserName = sm2.encry(self.M_UserName)
            self.C_Password = sm2.encry(self.M_PassWord)
            print(self.C_Password)
            #print(self.C_UserName)
            # 打包成josn
            rejo = enjosn.enjosn('1', self.M_UserName, '0', '0', '0', self.C_Password)
            print(rejo)
            # 调用发送给服务器的函数
            # 调用发送给服务器的函数
            self.servreback=transport.co(rejo)
            # 服务器返回信息并提取信息
            if self.servreback=="0":

                self.saveandqury = Save()
                self.saveandqury.getui()
                self.ui.close()
            else:
                try:
                    QMessageBox.information(self.ui, "error", "输入有误，请重新输入")
                except Exception as str:
                    print("输入错误 %s" % (str))
    def getUsername(self):
        return self.M_UserName
#登录界面密码的显示和隐藏
    def hideOrShow(self):
            self.logpwdindex=self.logpwdindex+1
            if self.logpwdindex%2==0:
               self.password.setEchoMode(QLineEdit.Password)
               self.hideorshow_btn.setIcon(QIcon("icon/preview-close-one.png"))
            else:
               self.password.setEchoMode(QLineEdit.Normal)
               self.hideorshow_btn.setIcon(QIcon("icon/preview-open.png"))
#注册界面的确认函数
    def emit_Confir_Button(self):
        if self.PassWordSure.text().strip() == '' or self.PassWord.text().strip() == '' or self.ui.UserName.text().strip() == '':
            try:
                QMessageBox.information(self.ui, "error", "输入有误，请重新输入")
            except Exception as str:
                print("输入错误 %s" % (str))
        elif len(self.PassWord.text()) < 6:
            QMessageBox.information(self.ui, "warning", "密码小于6位")
        elif self.PassWord.text() != self.PassWordSure.text():
            try:
                QMessageBox.information(None, "error", "两次密码输入不一致")
            except Exception as str:
                print("未知错误 %s" % (str))
        else:
            self.M_UserName = self.UserName.text()
            self.M_PassWord = self.PassWord.text()
            # 加密
            #self.C_UserName = sm2.encry(self.M_UserName)
            self.C_Password = sm2.encry(self.M_PassWord)
            print(self.C_Password)
            print(self.M_UserName)
            # 打包成josn
            rejo = enjosn.enjosn('0', self.M_UserName, '0', '0', '0', self.C_Password)
            # 调用发送给服务器的函数
            self.servreback=transport.co(rejo)

            # 服务器返回信息并提取信息
            if self.servreback=="0":
                QMessageBox.information(None, "提示", "注册成功")
            else:
                QMessageBox.information(None, "提示", "注册失败")


#注册界面取消回到登录的函数
    def changToLogin(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui1)
#注册界面密码的隐藏和显示
    def RegPwdhideOrShow(self):
        self.registindepwd = self.registindepwd + 1
        if self.registindepwd % 2 == 0:
            self.PassWord.setEchoMode(QLineEdit.Password)
            self.RegPwd_hors_btn.setIcon(QIcon("icon/preview-close-one.png"))
        else:
            self.PassWord.setEchoMode(QLineEdit.Normal)
            self.RegPwd_hors_btn.setIcon(QIcon("icon/preview-open.png"))

# 注册界面确认密码的隐藏和显示
    def PwdsurehideOrShow(self):
        self.registindexpwdsure = self.registindexpwdsure + 1
        if self.registindexpwdsure % 2 == 0:
            self.PassWordSure.setEchoMode(QLineEdit.Password)
            self.Pwdsure_hors_btn.setIcon(QIcon("icon/preview-close-one.png"))
        else:
            self.PassWordSure.setEchoMode(QLineEdit.Normal)
            self.Pwdsure_hors_btn.setIcon(QIcon("icon/preview-open.png"))
#注册界面的其他测试函数
    def emit_Username(self):
        print("UserName发生改变")
    def emit_Password(self):
        print("PassWord发生改变")
    def emit_ConPassword(self):
        print("ConPassword发生改变")



class Save:
    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('save1.ui')
        self.pwdindex=0
        self.queryindex=0
        #定义槽函数
        self.ui.create_btn.clicked.connect(self.create)  # 确认
        self.ui.submit_btn.clicked.connect(self.submit) #确认
        self.ui.hideorshow_btn.clicked.connect(self.hideOrShow)
        self.ui.passwd.setEchoMode(QLineEdit.Password)
        self.ui.tabWidget.currentChanged.connect(self.on_tab_changed)
        self.ui.comboBox.currentIndexChanged.connect(self.selectionchange)
        self.ui.query_Button.clicked.connect(self.query)
        self.ui.delete_Button.clicked.connect(self.delete)

        self.ui.tabWidget.setCurrentIndex(1)
        # 获取登录时的用户名
        self.user_name = glv.get('username')
#设计界面背景图片
        background_label = QLabel(self.ui.tabWidget)
        # 加载背景图片
        background_image = QPixmap("icon/qbackground.jpg")
        # 设置背景图片到QLabel上
        background_label.setPixmap(background_image)
        # 调整QLabel的大小以适应窗口
        background_label.setGeometry(0, 0, self.ui.width(), self.ui.height())
        background_label.lower()
    #显示密码与否的函数
    def hideOrShow(self):
            self.pwdindex=self.pwdindex+1
            if self.pwdindex%2==0:
               self.ui.passwd.setEchoMode(QLineEdit.Password)
               self.ui.hideorshow_btn.setIcon(QIcon("icon/preview-close-one.png"))
            else:
               self.ui.passwd.setEchoMode(QLineEdit.Normal)
               self.ui.hideorshow_btn.setIcon(QIcon("icon/preview-open.png"))
#生成界面的槽函数
    def create(self):
        #调生成的函数
        length = int(self.ui.pwdlength.text())
        passwdgen=pingce.appear(length)
        self.ui.passwd.setText(passwdgen)
        return passwdgen
    #获得的用户名的函数

   #提交按钮上传的函数
    def submit(self):
        # 接收其他数据
        if self.ui.notes.text().strip() == '' or self.ui.userid.text().strip() == '' or self.ui.pwdlength.text().strip() == '':
            try:
                QMessageBox.information(self.ui, "error", "输入有误，请重新输入")
            except Exception as str:
                print("输入错误 %s" % (str))
        else:
            self.notes = self.ui.notes.text()
            self.M_UserId = self.ui.userid.text()
            self.M_Passwd = self.ui.passwd.text()
            # 加密
            #C_UserName=sm2.encry(login.Stats.getUsername())
            self.C_UserId = sm2.encry(self.M_UserId)
            self.C_Password = sm2.encry(self.M_Passwd)
            print(self.C_Password)
            print(self.C_UserId)
            # 打包成josn
            rejo = enjosn.enjosn('2', self.user_name, self.C_UserId, self.C_Password, self.notes, '0')
            print(rejo)
            # 调用发送给服务器的函数
            # 调用发送给服务器的函数
            self.servreback=transport.co(rejo)
            print(self.servreback)
            # 服务器返回信息并提取信息
            if self.servreback=='0':
                QMessageBox.information(self.ui, "提示", "上传成功")
            else:
                QMessageBox.information(self.ui, "提示", "上传失败")
    #切换tab时的查询信号发送
    def on_tab_changed(self):
        self.queryindex=self.queryindex+1
        if self.queryindex % 2==1 :
            rejo = enjosn.enjosn('3', self.user_name, '0', '0', '0', '0')
            self.rebacklist=transport.co(rejo)
            print(type(self.rebacklist))
            self.de_rebacklist=enjosn.dejosn(self.rebacklist)
            print(self.de_rebacklist)
            self.addElement()

        else:
            print("存储")
#查询界面的槽函数
    def addElement(self):
         # 获取UI文件中的comboBox对象
        self.ui.comboBox.clear()
        self.list1=[]
        for i in self.de_rebacklist:
           self.list1.append(i[0])
        print(self.list1)
        self.ui.comboBox.addItems(self.list1)
    def selectionchange(self):
        self.option=self.ui.comboBox.currentText()
        print(self.option)
    def query(self):
        option = self.ui.comboBox.currentText()
        rejo = enjosn.enjosn('4', self.user_name, '0', '0', option, '0')
        self.reback=transport.co(rejo)
        self.de_re=enjosn.dejosn(self.reback)
        self.de_reback=self.de_re[0]
        self.re_userid=sm2.decry(self.de_reback[0])
        self.re_password=sm2.decry(self.de_reback[1])
        self.ui.user_ID.setText(self.re_userid)
        self.ui.pass_WORD.setText(self.re_password)
        print(self.de_reback)
        print(self.re_userid)
        print(self.re_password)

    def delete(self):
        option = self.ui.comboBox.currentText()
        rejo = enjosn.enjosn('5', self.user_name, '0', '0', option, '0')

        rebk=transport.co(rejo)
        if rebk=='0':
            rejo = enjosn.enjosn('3', self.user_name, '0', '0', '0', '0')
            self.rebacklist = transport.co(rejo)
            print(type(self.rebacklist))
            self.de_rebacklist = enjosn.dejosn(self.rebacklist)
            print(self.de_rebacklist)
            self.addElement()
        print(rejo)
    #总界面的函数
    def getui(self):
        self.ui.show()






app = QApplication(sys.argv)
stats = LogAndReg()
stats.ui.show()
sys.exit(app.exec())

