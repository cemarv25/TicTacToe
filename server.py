import socket
import os
from _thread import *

server_side_socket = socket.socket()
host = 'localhost'
port = 8080
thread_count = 0
clients = []

try:
    server_side_socket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening...')
server_side_socket.listen(2)


def multi_threaded_client(conn):

    while True:
        data = conn.recv(2048)
        print(data)
        if not data:
            break
        
        #Check which client we have
        if conn == clients[0]:
            clients[1].send(data)
        else:
            clients[0].send(data)

        #conn.send(data)
    if conn in clients:
        conn_index = clients.index(conn)
        clients.remove(conn_index)
    conn.close()


while True:
    client, add = server_side_socket.accept()
    clients.append(client)
    print('Connected to: ' + add[0] + ':' + str(add[1]))
    start_new_thread(multi_threaded_client, (client,))
    thread_count += 1
    print('Thread Number: ' + str(thread_count))
server_side_socket.close()
