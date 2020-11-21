import socket
import os
from _thread import *

server_side_socket = socket.socket()
host = 'localhost'
port = 8080
thread_count = 0

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
        conn.send(data)
    conn.close()


while True:
    client, add = server_side_socket.accept()
    print('Connected to: ' + add[0] + ':' + str(add[1]))
    start_new_thread(multi_threaded_client, (client,))
    thread_count += 1
    print('Thread Number: ' + str(thread_count))
server_side_socket.close()
