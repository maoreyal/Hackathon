import socket
import threading
import random
import scapy

class client():
    def __init__(self,team_name,destination_port =  13117) -> None:
        self.team_name = team_name
        self.destination_port = destination_port