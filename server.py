import socket
import threading
from game_logic import start_game
import os

def get_port_number():
    """
    Function to get the port number on which to run the server or use the default one
    """
    port_number = os.getenv("SOCKET_GAME_PORT", 6018)
    port_number = int(port_number)
    return port_number

def server_program():
    """
    Function to start the server and listen for new connection and start a new thread for each 
    connection
    """
    host = socket.gethostname()
    port = get_port_number()

    server_socket = socket.socket() 

    server_socket.bind((host, port))

    server_socket.listen(1000)
    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        threading.Thread(target=start_game, args=[conn, address]).start()

if __name__ == '__main__':
    server_program()
