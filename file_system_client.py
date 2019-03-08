#! /usr/bin/env python3
# -*- coding:utf-8 -*-

#file system client
from socket import * 
import sys,time

#确认网络地址
HOST = '127.0.0.1'
PORT = 9553
ADDR = (HOST,PORT)

#具体功能
class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd
    #查看所有文件
    def do_list(self):
        #发送L请求
        self.sockfd.send(b'L')
        #等待server回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            #只能显示4096字节
            data = self.sockfd.recv(4096).decode()
            #把收到的字符串以','分割为列表
            files = data.split(',')
            for file in files:
                print(file)
        else:
            #无法完成操作
            print(data.decode())
    #client exit
    def do_quit(self):
        #给服务端发Q
        self.sockfd.send(b'Q')
        #关闭c套接字
        self.sockfd.close()
        #退出子进程
        sys.exit('Thanks,bye')
    #下载文件
    def do_get(self,filename):
        #给服务端发G类请求 包括文件名
        self.sockfd.send(('G '+filename).encode())
        #等待server回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            #接受文件内容
            fd = open(filename,'wb')
            while True:
                data = self.sockfd.recv(1024)
                #约定的结束标志
                if data == b'##':
                    print('下载成功')
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)
    #上传文件
    def do_put(self,filename):
        #判断这个文件存不存在
        try:
            f = open(filename,'rb')
        except IOError:
            print('没有该文件')
            return 
        #只要文件名,不要路径
        filename = filename.split('/')[-1]
        #给服务器发送P类请求 不包括文件路径
        self.sockfd.send(('P '+filename).encode())
        #等待server回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            #上传文件内容
            while True:
                data = f.read(1024)
                self.sockfd.send(data)
                if not data:
                    #防止粘包
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    break 
            f.close()
            print('文件上传成功')
        else:
            print(data)
        




#网络连接
def main():
    #创建套接字
    sockfd = socket()
    try:
        #发起连接
        sockfd.connect(ADDR)
    except Exception as e:
        print('connect Error:',e)
        return 
    #创建文件处理类对象
    ftp = FtpClient(sockfd)

    while True:
        menu = '''------file system-------
        1-list
        2-get filename
        3-put filename
        4-quit\n-----------------------'''
        print(menu)
        cmd = input('please input>>')
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd.strip() == 'quit':
            ftp.do_quit()
        elif cmd[:3] == 'get':
            filename = cmd.strip().split(' ')[-1]
            ftp.do_get(filename)
        #上传文件
        elif cmd[:3] == 'put':
            #切割出文件路径
            filename = cmd.strip().split(' ')[-1]
            print(filename)
            ftp.do_put(filename)

        else:
            print('请输入正确命令')



#测试
if __name__ == '__main__':
    main()
