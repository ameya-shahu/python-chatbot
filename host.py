import socket
import apiai
import json

#class 'ClientChattingServer' has functions related to local chatting server within the network.
class ClientChattingServer:

    #function 'start_server' will start server at port 8080
    def start_server(self):
        self.server_name = socket.socket()  # object of socket class
        self.hostname = socket.gethostname() #To get hostname
        self.port = 8080                     #port use to run service is 8080
        self.server_name.bind((self.hostname, self.port)) #binding host and port
        self.server_name.listen(1)           #at a time 1 client can interact with server.
        print('I am svailable at', self.hostname) #Display hostname for client to connect

    #function 'listen_connection' will connect with client
    def listen_connection(self):
        self.connection, self.address = self.server_name.accept()  #accept client request to connect to server
        if self.connection != None:
            print("I am connected at", self.address)
        self.send_msg("hi,how can I help you?") #As soon as client connect server will initiate chat

    #function 'send_msg' use to send message to client in local network
    def send_msg(self, message):
        message = message.encode() #message need to 'encode' in bytes to send on network
        self.connection.send(message) #message will be send on network

    # function 'receive_msg' use to receive message from client in local network
    def recieve_msg(self):
        try:
            message = self.connection.recv(1024).decode() #message will be received upto 1024bytes and decode into utf-8
            return message
        except ConnectionResetError:
            exit()

'''For this project dialogflow (previously Api.ai) is used for Natural Language Processing (NLP).
 user need to login in dialogflow console and create and train agent according to requirement.
 'CLIENT ACCESS TOKEN' will require to connect server with Dialogflow.'''
class DialogflowServer:
    #function 'dialogflow_connect' will use to connect with Dialogflow console
    def dialogflow_connect(self,CLIENT_ACCESS_TOKEN):
        self.CLIENT_ACCESS_TOKEN = CLIENT_ACCESS_TOKEN
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)#use to connect with agent with given CLIENT ACCESS TOKEN
        self.request = self.ai.text_request()
        self.request.lang = 'de'  # use defult langauge
        self.request.session_id = "<SESSION ID,UNIQUE FOR EACH USER>"

    def bot_query(self, message):
        self.request.query = message  # sending query to dialogflow
        response = self.request.getresponse()  # geting response from diallogflow
        message = response.read()  # reading HTTPResponse to bytes
        struct = json.loads(message.decode())  # decoding bytes in utf-8 and converting JSON to python dictionary
        reply = struct['result']['fulfillment']['speech']  # reading value of key
        return reply


if __name__ == "__main__":
    Dialogflow_Acess_Token = input('Enter CLIENT ACCESS TOEKN: ')
    dialogflow_server = DialogflowServer() #use to connect dialogflow

    server = ClientChattingServer()     # chatting client server
    server.start_server()               # this will start server
    server.listen_connection()

    while True:
        dialogflow_server.dialogflow_connect(Dialogflow_Acess_Token)      #you need to connect every time in every loop as section ID changes
        message = server.recieve_msg()                    #reciving message from client
        print("Client:" + message)
        dialogflow_message = dialogflow_server.bot_query(message) #forwading message to dialogflow console
        print("Server:"+dialogflow_message)
        if 'bye' in message:    #conversation will end with 'bye' message from client
            break
        else:
            server.send_msg(dialogflow_message)



