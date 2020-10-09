import socket
import json
import os
from select import select
import sys

def get_port_number():
    port_number = os.getenv("SOCKET_GAME_PORT", 6018)
    port_number = int(port_number)
    return port_number

def client_program():
    host = socket.gethostname()
    port = get_port_number()

    client_conn = socket.socket()

    client_conn.connect((host, port))

    while True:
        data = client_conn.recv(1024).decode()
        print(data)
        data = json.loads(data)
        if "timeout" in data:
            text = data["text"]
            timeout = data["timeout"]
            print("You have %s seconds for this round\nYour character is %s" % (timeout, text))
            rlist, _, _ = select([sys.stdin], [], [], timeout)
            if rlist:
                for input_device in rlist:
                    if input_device == sys.stdin:
                        user_input = sys.stdin.readline().strip()
                        client_conn.send(user_input.encode())
        elif "skip" in data:
            reason = data["reason"]
            score = data["score"]
            print("Chance skipped. Your score is now %s\n" % score)
        elif "match" in data:
            match_value = data["match"]
            score = data["score"]
            if match_value == True:
                print("That is a correct match! Your score is now %s\n" % score)
            else:
                print("That is an incorrect match! Your score is now %s\n" % score)
        elif "gameover" in data:
            reason = data["reason"]
            score = data["score"]
            print("\n=======================")
            print("Game is over due : %s and your final score is: %s" % (reason, score))
            print("=======================")
            break

    client_conn.close()


if __name__ == '__main__':
    client_program()
