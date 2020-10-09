import random
import string
from select import select
import json
import time

MAX_RETIRES = 3
MIN_SCORE = -3
MAX_SCORE = 10


def send_json(conn, data):
    """
    Function to encode dictionary and send through the socket connection
    """
    data = json.dumps(data).encode()
    time.sleep(0.1)
    conn.send(data)

def start_game(conn, address):
    """
    Main function which contains the logic for the game
    """
    score = 0
    timeout_retries = 0
    while True:
        random_timeout = random.randint(3, 10)

        random_string = random.choice(string.ascii_letters)

        data = {"timeout": random_timeout, "text": random_string}
        send_json(conn, data)

        rlist, _, _ = select([conn], [], [], random_timeout)
        if rlist:
            recieved_data = conn.recv(1024).decode().strip()
            if random_string == recieved_data:
                score += 1
                result = {"match": True, "score": score}
                send_json(conn, result)
            else:
                score -= 1
                result = {"match": False, "score": score}
                send_json(conn, result)
            timeout_retries = 0
        else:
            result = {"skip": True, "reason": "timeout", "score": score}
            timeout_retries += 1
            send_json(conn, result)

        if timeout_retries == MAX_RETIRES:
            result = {"gameover": True, "reason": "timeout", "score": score}
            send_json(conn, result)
            break

        if score == MIN_SCORE or score == MAX_SCORE:
            result = {"gameover": True, "reason": "score", "score": score}
            send_json(conn, result)
            break

    conn.shutdown()
    conn.close()
