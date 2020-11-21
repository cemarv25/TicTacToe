import pygame
import os
import socket
import threading
from grid import Grid

os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'  # screen display position
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Tic-tac-toe")
grid = Grid()
player = "X"
turn = True
playing = "True"
client_multi_socket = socket.socket()

host = "localhost"
port = 8080

print('Waiting for connection response')
try:
    client_multi_socket.connect((host, port))
except socket.error as e:
    print(str(e))


def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


def receive_data():
    global turn
    while True:
        try:
            data = client_multi_socket.recv(1024).decode()
            data = data.split('-')
            print(data)
            posx, posy = int(data[0]), int(data[1])
            if data[2] == 'yourturn':
                turn = True
            if data[3] == 'False':
                grid.game_over = True
            if grid.get_cell_value(posx, posy) == 0:
                grid.set_cell_value(posx, posy, 'O')
        except socket.error as e:
            str(e)


create_thread(receive_data)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            # index 0 : left mouse button, 1 : middle mouse button, 2 : right mouse button
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    cell_x = pos[0] // 200
                    cell_y = pos[1] // 200
                    grid.get_mouse(cell_x, cell_y, player)
                    if grid.game_over:
                        playing = 'False'
                    send_data = '{}-{}-{}-{}'.format(cell_x,
                                                     cell_y, 'yourturn', playing).encode()
                    client_multi_socket.send(send_data)
                    turn = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.reset_game()
                playing = 'True'
            elif event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((255, 255, 255))
    grid.draw(screen)
    pygame.display.flip()
