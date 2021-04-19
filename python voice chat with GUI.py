import socket
import threading
import pyaudio
import os
import pyautogui


#client class
class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        while 1:
            try:
                self.target_ip = pyautogui.prompt('Enter server IP:')
                self.target_port = int(pyautogui.prompt('Enter target port of server : '))

                self.s.connect((self.target_ip, self.target_port))

                break
            except:
                pyautogui.alert("Couldn't connect to server")
                exit()

        chunk_size = 1024 # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        
        connect_server = pyautogui.confirm('Connected to Server', buttons=['Close Program'])
        if connect_server == 'Close Program':
            exit()

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
            self.ip = '127.0.0.1' #You can Change Host IP  
            while 1:
                try:
                    self.port = int(pyautogui.prompt('Enter port number to run on : '))

                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s.bind((self.ip, self.port))

                    break
                except:
                    pyautogui.alert("Couldn't bind to that port")
                    exit()

            self.connections = []
            self.accept_connections()

    def accept_connections(self):
        self.s.listen(100)

        con = pyautogui.confirm('Running on IP: '+self.ip+':'+str(self.port), buttons=['Close Server'])
        if con == 'Close Server':
            exit()
        
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

def call():
    button = pyautogui.confirm('Choose an action', buttons =['Server Side', 'Client Side'])
    if button == 'Server Side':
        Server()
    elif button == 'Client Side':
        Client()

call()