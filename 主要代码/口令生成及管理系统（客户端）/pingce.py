#python 3.9
import string
import random
import re
"""
补充String模块中的常量：
小写字母：string.ascii_lowercase；
大写字母：string.ascii_uppercase；
数字：string.digits；
标点符号：string.punctuation
"""

# 将string的几大字符串拼接在一起，作为候选


#print("可使用字符：",end='')
list0=list('1234567890')
list1=list('qwertyuiopasdfghjklzxcvbnm')
list2=list(r"`~\!@#$%^&*()_-+=|{}[]:;>?/',.")
list2.append('"')
#合法性
def legal(p):
    list3=[i.upper() for i in list1]
    if not set(p).difference(list0,list1,list2,list3):
        print("Your passsword is legal.")
        return True
    else:
        print("Your passsword is illegal.")
        return False


# 奖励累加变量，满足大小写字母混合，变量+1
reward = 0


# 密码长度
def len_password(p):
    if len(p) <= 4:
        return 5
    elif len(p) <= 7:
        return 10
    else:
        return 25


# 字母
def letter(p):
    count = 0
    i_list = []
    for i in p:
        if i.isalpha():
            count += 1
            i_list.append(i)
    if count == 0:
        return 0
    elif str(i_list).upper() == str(i_list) or str(i_list).lower() == str(i_list):
        return 10
    else:
        return 20
        # 大小写混合，奖励+1
        reward += 1


# 数字
def number(p):
    num_list = []

    for i in p:
     try:
        if int(i):
            num_list.append(i)
        else:
            pass
     except:
         pass
    if not num_list:
        return 0
    elif len(num_list) < 3:
        return 10
    else:
        return 20


# number("1123wde")

def symbol(p):
    a = set(p).difference(list0, list1)
    if not a:
        return 0
    elif len(a) == 1:
        return 10
    else:
        return 25
# print(symbol("123e3238??!"))

def appear(l):
    while (1):
          words = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    # 根据长度随机采样几个字符，得到一个列表
          chosen = random.sample(words, l)
    # 将列表的每个元素，拼接成一个大字符串
          password = "".join(chosen)
          if legal(password):
              # 没试过这样偷懒的方法，今天试试
              func_list = [len_password(password), letter(password), number(password), symbol(password)]
              # 奖励加入，逻辑完全依照规则
              if reward == 1 and func_list[2] != 0 and func_list[3] != 0:
                  func_list.append(5)
              elif func_list[1] != 0 and func_list[2] != 0:
                  func_list.append(2)
              elif func_list[1] + func_list[2] + func_list[3] == 0:
                  func_list.append(3)
              else:
                  pass
              total = sum(func_list)
              print("总分数：", total)
              print("您的密码强度等级：", end='')
              if total >= 90:
                  print("非常安全")
                  return password
              elif total >= 80:
                  print("安全")
              elif total >= 70:
                  print("非常强")
              elif total >= 60:
                  print("强")
              elif total >= 50:
                  print("一般")
              elif total >= 25:
                  print("弱")
              else:
                  print("非常弱")
          else:
              continue
