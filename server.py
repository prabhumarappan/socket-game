import socket
import threading
from game_logic import start_game


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 6014

    server_socket = socket.socket()  # get instance

    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1000)
    while True:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        threading.Thread(target=start_game, args=[conn, address]).start()


if __name__ == '__main__':
    server_program()
