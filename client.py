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

    def __init__(self, client_port=56417, destination_port=45654, client_name='Dr.Stark') -> None:
        self.client_buffer_size = 1024
        self.client_port = client_port
        self.client_name = client_name
        self.udp_port = destination_port
        self.in_game = None

        print("Client started, listening for offer requests...")

    def connecting(self):
        UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDP_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        UDP_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        UDP_client.bind(('', self.udp_port))
        #UDP_client.bind(('', self.client_port))
        #while self.in_game is None:
        while True:
            UDP_client.settimeout(1)
            try:
                print('in while')
                bytes1, ADDR = UDP_client.recvfrom(self.client_buffer_size)
                print(ADDR)
                cookie, msg_type, server_port = struct.unpack('IbH', bytes1)
                print('2')
                
            except:
                print('1')
                continue
            # print(cookie == '0xabcddcba')
            # if cookie == '0xabcddcba' and msg_type == '0x2':
            print(f"Received offer from {ADDR[0]}, attempting to connect...")
            TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('hi')
            self.in_game = True


            try:
                print('shit')
                print(ADDR[0])
                TCP_socket.connect(ADDR[0], server_port)
                #return TCP_socket
                print('error')
                TCP_socket = self.connecting()
                group_name = self.client_name + '\n'
                TCP_socket.sendall(group_name.encode())
                print("error1")
                print(TCP_socket.recv(self.client_buffer_size).decode('UTF-8'))

                answer = keyboard.read_key()
                tcp_socket.sendall(answer.encode())
                print("error2")
                print(tcp_socket.recv(self.client_buffer_size).decode('UTF-8'))
                tcp_socket.close()
                return
            except:
                print('fail to connect')
        #return TCP_socket
            

    # def play_game(self):
        # tcp_socket = self.connecting()
        # group_name = self.client_name + '\n'
        # tcp_socket.send(group_name.encode())

        # print(tcp_socket.recv(self.client_buffer_size).decode('UTF-8'))

        # answer = keyboard.read_key()
        # tcp_socket.sendall(answer.encode())

        # print(tcp_socket.recv(self.client_buffer_size).decode('UTF-8'))



client = Client()
while True:
    #client.play_game()
    connection = client.connecting()
    #connection.close()