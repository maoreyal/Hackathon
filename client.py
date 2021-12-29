import socket
import random
# import scapy
import threading
# import sys
# import select
import keyboard
# from scapy.all import get_if_addr
import struct

class Client:

    def init(self, destination_port=12111, client_port=4565, client_name='Dr.Stark') -> None:
        # self.server_ip_address = socket.gethostbyname(socket.gethostname())
        self.udp_port = destination_port
        self.client_buffer_size = 1024
        self.client_port = client_port
        self.client_name = client_name

        print("Client started, listening for offer requests...")

    def connecting(self):
        UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDP_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #print('error 1')
        UDP_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        #print('error 2')
        UDP_client.bind(('', self.udp_port))
        #print('error 3')
        bytes1, ADDR = UDP_client.recvfrom(self.client_buffer_size)

        cookie, msg_type, server_port = struct.unpack('IbH', bytes1)
        if cookie == '0xabcddcba' and msg_type == '0x2':
            print(f"Received offer from {ADDR[0]}, attempting to connect...")
            TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                TCP_socket.connect((socket.gethostname(), server_port))
            except:
                return None
            return TCP_socket

    def play_game(self):
        tcp_socket = self.connecting()
        group_name = self.client_name + '\n'
        tcp_socket.send(group_name.encode())

        print(tcp_socket.recv(self.client_buffer_size).decode('UTF-8'))

        answer = keyboard.read_key()
        tcp_socket.sendall(answer.encode())

        print(tcp_socket.recv(self.client_buffer_size).decode('UTF-8'))




client = Client()
while True:
    client.play_game()
    connection = client.connecting()
    connection.close()