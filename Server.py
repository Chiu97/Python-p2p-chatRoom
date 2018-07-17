#coding:utf-8

import socketserver,json

connLst = []
##  连接列表，用来保存一个连接的信息（代号 地址和端口 连接对象）
class Connector(object):#连接对象类
    def __init__(self,account,identify,addrPort,conObj):
        #客户端名
        self.account = account
        #客户端标识，区别客户与客服
        self.identify = identify
        #客户端端口+地址
        self.addrPort = addrPort
        self.conObj = conObj



class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        print("got connection from",self.client_address)
        register = False
        while True:
            conn = self.request
            data = conn.recv(1024)
            if not data:
                continue
            dataobj = json.loads(data.decode('utf-8'))
            #如果连接客户端发送过来的信息格式是一个列表且注册标识为False时进行用户注册
            if type(dataobj) == list and not register:
                account = dataobj[0]
                identify = dataobj[1]
                conObj = Connector(account,identify,self.client_address,self.request)
                connLst.append(conObj)
                register = True
                continue
            print(connLst)
            #如果目标客户端在发送数据给目标客服端
            if len(connLst) > 1 and type(dataobj) == dict:
                sendok = False
                for obj in connLst:
                    if dataobj['to'] == obj.account:
                        obj.conObj.sendall(data)
                        sendok = True
                if sendok == False:
                    print('no target valid!')
            else:
                conn.sendall('nobody recevied!'.encode('utf-8'))
                continue

class TcpServer:
    def __init__(self):
        server = socketserver.ThreadingTCPServer(('127.0.0.1', 5000), MyServer)
        print('waiting for connection...')
        server.serve_forever()


if __name__ == '__main__':
    TcpServer()
