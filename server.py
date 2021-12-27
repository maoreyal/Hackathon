import socket
import threading
import random
import time
import struct
#import getch

class server():
    def __init__(self, destination_port = 13117) -> None:
        self.server_ip_address = socket.gethostbyname(socket.gethostname())
        self.cookie = 0xabcddcba
        self.messagetype = 0x2
        self.destination_port = destination_port
        self.client_counter = 0

    def Run_Game(self):
        # in general purpose
        UDP_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        UDP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        ADDR = (self.server_ip_address,self.destination_port)
        UDP_socket.bind(ADDR)
        while True:
            print(f'“Server started, listening on IP address {self.server_ip_address}')
            #waiting_for_clients real function
            while self.client_counter<2:
                message = struct.pack('ich',(self.cookie,self.messagetype,42069))
                UDP_socket.sendto(message,('<broadcast>',self.destination_port))
                time.sleep(1)
            #ends hereee
            
            