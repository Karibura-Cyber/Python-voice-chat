import socket
import threading
import pyaudio


#client class
class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        while 1:
            try:
                self.target_ip = input('Enter IP address of server --> ')
                self.target_port = int(input('Enter target port of server --> '))

                self.s.connect((self.target_ip, self.target_port))

                break
            except:
                print("Couldn't connect to server")

        chunk_size = 1024 # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        
        print("Connected to Server")

        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        self.send_data_to_server()

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass


    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass
#end client class

#server class
class Server:
    def __init__(self):
            self.ip = float(input('Server IP: '))
            while 1:
                try:
                    self.port = int(input('Enter port number to run on --> '))

                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s.bind((self.ip, self.port))

                    break
                except:
                    print("Couldn't bind to that port")

            self.connections = []
            self.accept_connections()

    def accept_connections(self):
        self.s.listen(100)

        print('Running on IP: '+self.ip)
        print('Running on port: '+str(self.port))
        
        while True:
            c, addr = self.s.accept()

            self.connections.append(c)

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()
        
    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                except:
                    pass

    def handle_client(self,c,addr):
        while 1:
            try:
                data = c.recv(1024)
                self.broadcast(c, data)
            
            except socket.error:
                c.close()
#end server class

#function call statement

def call():
    print('_________________________   _____________')
    print('\______   \__    ___/\   \ /   /\_   ___ \ ')
    print(' |     ___/ |    |    \   Y   / /    \  \/')
    print(' |    |     |    |     \     /  \     \____')
    print(' |____|     |____|      \___/    \______  /')
    print('                                        \/')
    print('')
    print('Python Voice Chat Develop By Karibura')
    print('')
    print('Server side [1]\nClient side [2]\nExit [3]\n')
    i = int(input("Enter Number: "))
    print('\n')
    if i == 1:
        server = Server()
    elif i == 2:
        client = Client()
    elif i == 3:
        print('See you Again')
    else:
        print('please Enter a number')
    


call()

#end function call statement