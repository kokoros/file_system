Project:file_system(文件管理器)
===================

Getting Started
--------------
* 设置文件目录:  
  修改file_system_server.py中的第14行  
FILE_PATH = '../../twostage_note_MySQL/twotest/'

* 进入目录: 
     cd file_system
* 开启服务端:
     python3 file_system_server.py

Prerequisites(先决条件)
----------------------
* python3
* pip3 socket 

Running the tests
-----------------
* 开启服务端后再开启客户端:
  python3 file_system_client.py
* 可以开启多个客户端

Function
------------------
普通文件服务器 
>>功能:
1.查看设置的目标内所有普通文件列表  
    2.下载文件    
    3.上传文件  
    4.退出系统

Built With
------
* python3
* socket

Authors
-----------
* Koro
