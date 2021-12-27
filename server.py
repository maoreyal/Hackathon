import socket
import threading
import random
import time

class server():
    def __init__(self, destination_port = 13117) -> None:
        self.server_ip_address = socket.gethostbyname(socket.gethostname())
        self.cookie = 0xabcddcba
        self.message = 0x2
        self.destination_port = destination_port


    def waiting_for_clients(self):
        while True:
            print(f'“Server started, listening on IP address {self.server_ip_address}')
            UDP_socket = socket.socket(socket.AF_INET,socket.NI_DGRAM)
            time.sleep(1)
            ADDR = (self.server_ip_address,self.destination_port)