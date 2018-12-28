# server.py
# 从wsgiref模块导入:
from wsgiref.simple_server import make_server
# 导入我们自己编写的application函数:
from hello import application

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
<<<<<<< HEAD
httpd = make_server('172.16.181.146', 8000, application)
=======
httpd = make_server('107.182.26.148', 8000, application)
>>>>>>> 23cc6eeb6d17e525fd728f81a19d5ba110649ceb
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()
