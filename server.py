import socket
import random
import string
from select import select


def server_program():
    # get the hostname
    host = socket.gethostname()
    print(host)
    port = 6006  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    score = 0
    while True:
        random_string = random.choice(string.ascii_letters)
        data = random_string + "\n"
        conn.send(data.encode())  # send data to the client
        # receive data stream. it won't accept data packet greater than 1024 bytes
        timeout = 5
        rlist, wlist, xlist = select([conn], [], [], timeout)
        if rlist:
            recieved_data = conn.recv(1024).decode().strip()
            if random_string == recieved_data:
                score += 1
                result = "Matched the sent! score is now %s\n" % score
                conn.send(result.encode())
            else:
                score -= 1
                result = "does not match the sent! score is now %s\n" % score
                conn.send(result.encode())
        else:
            result = "Timed out!\n"
            conn.send(result.encode())

        if score == -3 or score == 10:
            data = "Game Over! Your score is %s\n" % score
            conn.send(data.encode())
            break

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()