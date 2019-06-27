import socket


class client:
    #function 'connect_server' use to connect with given host
    def connect_server(self,host):
        self.connection = socket.socket()
        self.host = host
        self.port = 8080      #use port 8080 for chatting
        self.connection.connect((self.host,self.port))#connect at given server address and givem port

    # function 'send_msg' use to send message to client in local network
    def send_msg(self, message):
        message = message.encode()#message need to 'encode' in bytes to send on network
        self.connection.send(message)

    # function 'receive_msg' use to receive message from client in local network
    def receive_msg(self):
        message = self.connection.recv(1024).decode()#message will be received upto 1024bytes and decode into utf-8
        return message

if __name__ == "__main__":
    host = input("enter Teacher's server name: ") #take inpur host name or ip address to connect
    student = client()
    student.connect_server(host)    #connect with host
    while True:
        recv_msg = student.receive_msg() #receive message from server
        print("Teacher:"+recv_msg)
        message = input("Student:") #take message input
        student.send_msg(message)
        if 'bye' in message: #if client send bye message,conversation will be end
            break


