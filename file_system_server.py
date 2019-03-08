#! /usr/bin/env python3
# -*- coding:utf-8 -*-

#file system server
from socket import * 
import os,sys,signal,time
#全局变量

#确认网络地址
HOST = '0.0.0.0'
PORT = 9553
ADDR = (HOST,PORT)
#确认目录路径
FILE_PATH = '../../twostage_note_MySQL/twotest/'

#具体功能的实现类
class FtpServer(object):
    def __init__(self,connfd):
        self.connfd = connfd 
    #查看所有普通文件名
    def do_list(self):
        #获取所有文件列表
        file_list = os.listdir(FILE_PATH) 
        #判断文件列表是否为空,给客户端发反馈消息
        if not file_list:
            self.connfd.send('文件库为空'.encode())
            return 
        else:
            self.connfd.send(b'OK')
            #因为连着发了两次send，防止TCP粘包,建立延迟
            time.sleep(0.1)
        files = ''
        for file in file_list:
            #去除隐藏和非普通文件
            if file[0] != '.' and os.path.isfile(FILE_PATH+file):
                files = files + file + ','
        #将拼接好的字符串传给client
        self.connfd.send(files.encode())
    #下载文件
    def do_get(self,filename):
        try:
            #试图打开文件
            fd = open(FILE_PATH+filename,'rb')
        except IOError:
            self.connfd.send('文件不存在'.encode())
            return 
        else:
            self.connfd.send(b'OK')
            #防止粘包,睡一下
            time.sleep(0.1)
        #发送文件内容
        while True:
            data = fd.read(1024)
            if not data:
                #连续发送,防止粘包
                time.sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)
    #上传文件
    def do_put(self,filename):
        #判断是否存在同名的文件
        if os.path.exists(FILE_PATH+filename):
            self.connfd.send('该文件已存在'.encode())
            return 
        #创建该文件
        fd = open(FILE_PATH+filename,'wb')
        self.connfd.send(b'OK')
        #接受文件内容
        while True:
            data = self.connfd.recv(1024)
            if data == b'##':
                break 
            fd.write(data)
        fd.close()

#对client请求做出回应
def do_request(connfd):
    #实例化一个功能性的类对象
    ftp = FtpServer(connfd)
    while True:
        #获取客户端请求
        data = connfd.recv(1024).decode()
        #为了防止报错,把not data 提前.因为client非常理退出时会发个空值过来
        if not data or data[0] == 'Q':
            connfd.close()
            return
        elif data[0] == 'L':
            ftp.do_list()
        elif data[0] =='G':
            filename = data.split(' ')[-1]
            ftp.do_get(filename)
        elif data[0] == 'P':
            filename = data.split(' ')[-1]
            ftp.do_put(filename)

#网络搭建
def main():
    #创建TCP套接字
    sockfd = socket()
    #重置端口
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    #绑定网络地址
    sockfd.bind(ADDR)
    #设置为监听套接字
    sockfd.listen(5)
    print('Waiting Listen 9553 Client...')
    #忽略子进程退出信号
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            #等待client连接
            connfd,addr = sockfd.accept()
        except KeyboardInterrupt:
            sys.exit('server exit')
        except Exception as e:
            print('Error:',e)
            continue
        print('client from:',addr)
        #创建子进程处理客户端请求
        pid = os.fork()
        #子进程
        if pid == 0:
            #关闭监听套接字
            sockfd.close()
            #对客户端请求做出处理
            do_request(connfd)
            #退出子进程
            os._exit(0)
        #父进程或者未创建子进程
        else:
            #关闭c套接字,继续等待client连接
            connfd.close()

if __name__ == '__main__':
    main()               




