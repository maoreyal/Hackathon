import socket
import threading
import InteruptableThread
import random
import time
import struct
from colorama import Fore, Back
#import getch

class Server():
    def __init__(self, destination_port = 13117,server_port = 45654) -> None:
        #server initialization
        self.server_ip_address = socket.gethostbyname(socket.gethostname())
        self.udp_port = destination_port
        self.server_buffer_size = 1024
        self.cookie = 0xabcddcba
        self.messagetype = 0x2
        self.server_port = server_port

        #clients that will be connected to the servers
        self.first_client, self.second_client = None, None
        self.second_client_join_time = None

        print(f'“{Fore.MAGENTA}Server started, listening on IP address {self.server_ip_address}"')

    def udp_broadcast(self):
        # server making udp brodcasting to players to join
        UDP_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        UDP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        ADDR = (self.server_ip_address,self.server_port)
        UDP_socket.bind(ADDR)
        
        message = struct.pack('Ibh',self.cookie,self.messagetype,self.udp_port)
        
        while not(self.first_client and self.second_client):
            UDP_socket.sendto(message,('<broadcast>',self.server_port))
            time.sleep(1)

        UDP_socket.close()

    def establishingTCP_with_players(self):
        #creating tcp connection
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.server_ip_address,self.server_port))
        #setting max queue connection to the server
        server_socket.listen(2)

        def adding_clients_to_server(accept):
            while not(self.first_client is None and self.second_client is None):
                client_socket, address = accept
                if self.first_client is None and self.second_client is None:
                    self.first_client = (client_socket, address)

                elif self.first_client is not None and self.second_client is None:
                    self.second_client = (client_socket, address)
                    self.second_client_join_time = time.time()

        thread = threading.Thread(target=adding_clients_to_server,args=(server_socket.accept, ))
        thread.start()

    def get_first_answer_and_team(self):
        def thread_answer_func(client_socket,team_name):
            try:
                clinet_answer = client_socket.recv(self.server_buffer_size).decode('utf-8')
                if clinet_answer is not None:
                    answer_and_team = (clinet_answer,team_name)
                    answer_and_team_list.append(answer_and_team)
            except:
                pass

        first_thread = InteruptableThread.InteruptableThread(target=thread_answer_func,args=(self.first_client[0],'first_team'))
        second_thread = InteruptableThread.InteruptableThread(target=thread_answer_func,args=(self.second_client[0],'second_team'))

        answer_and_team_list = list()

        first_thread.start()
        second_thread.start()

        time_limit = time.time() + 10
        while time.time() < time_limit:
            if answer_and_team_list != []:
                try:
                    first_thread.stop()
                    second_thread.stop()
                    result_and_team = answer_and_team_list[0]
                except:
                    print('Error were found within the system')
                
                return result_and_team

        #if we pass the time limit we will return None =
        return None

    def generate_math_question_and_result(self):
        
        opirations_list = ['+','-','*','/']
        curr_oprator = random.sample(opirations_list,1)[0]
        
        num1 = random.randint(-10000,10000)
        if curr_oprator == '+':
            if num1 > 9:
                num2 = random.randint(-num1, -num1+9)
            else:
                num2 = random.randint(0, 9-num1)
            result = (num1 + num2)
            

        if curr_oprator == '-':
            if num1 > 9:
                num2 = random.randint(0, 9 - num1)
            else:
                num2 = random.randint(num1, num1 + 9)
            result = (num1 - num2)
            

        if curr_oprator == '*':
            num1 = random.randint(-9, 9)
            if num1 > 0:
                num2 = random.randint(0, int(10/num1))
            else:
                num2 = random.randint(-int(10/num1), 0)
            result = (num1 * num2)
            

        if curr_oprator == '/':
            sign = ['+','-']
            l = random.sample(sign, 1)[0]
            num1 = random.randint(1, 1000)
            x = [num1]
            for i in range(1, num1):
                ans = num1 / i
                if (ans) % 1 == 0:
                    if ans < 10:
                        x.append(i)
            num2 = random.sample(x, 1)[0]
            if l == '-':
                result = -num1 / -num2
            else:
                result = num1/num2
            

        question = str(num1)+curr_oprator+str(num2)

        return question, result
        


    def game_stage(self):

        first_team = self.first_client[0].recv(self.server_buffer_size).decode()
        second_team = self.second_client[0].recv(self.server_buffer_size).decode()
        winning_team = ''

        question, math_result = self.generate_math_question_and_result()

        encoded_greeting_message = f"""
        Welcome to Quick Maths.
        {Fore.CYAN}Player 1: {first_team}
        {Fore.BLUE}Player 2: {second_team}
        ==
        Please answer the following question as fast as you can:
        {Back.MAGENTA}How much is {question}?""".encode()
        #wating 10 seconds after the second client joins
        while time.time <= self.second_client_join_time + 10:
            time.sleep(0.1)
            if time.time() >= self.second_client_join_time + 10:
                break
        
        self.first_client[0].send(encoded_greeting_message) # ask question 
        self.second_client[0].send(encoded_greeting_message) # ask question 
        
        answer_and_team = self.get_first_answer_and_team()
        if answer_and_team is None: 
            finish_game_with_draw = f"""Game over!
        The correct answer was {math_result}!
        Game finished with a DRAW!
        """.encode() 
            # send draw message
            self.client1[0].send(finish_game_with_draw)
            self.client2[0].send(finish_game_with_draw) 

        else:            
            client_answer, group_name = answer_and_team

            if client_answer.isdigit():
                client_answer = int(client_answer)
            else:
                client_answer = -1000

            result_is_matched = bool(client_answer == math_result)

            if group_name == 'first_team': 
                if result_is_matched:
                    winning_team = first_team
                else:
                    winning_team = second_team
            else:
                if result_is_matched:
                    winning_team = second_team
                else:
                    winning_team = first_team

            finish_game_with_win = f"""Game over!
                The correct answer was {math_result}!
                Congratulations to the winner: {winning_team}
                """.encode()
            # send finish message to groups
            self.first_client[0].send(finish_game_with_win)
            self.second_client[0].send(finish_game_with_win) 
        
server = Server()
while True:
    server.udp_broadcast()
    server.establishingTCP_with_players()
    server.game_stage()
    server.first_client[0].close()
    server.second_client[0].close()
    server.first_client = None
    server.second_client = None
    server.second_client_join_time = None
    print('Game over, sending out offer requests...')



