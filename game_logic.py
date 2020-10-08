import random
import string
from select import select

def start_game(conn, address):
    score = 0
    while True:
        random_string = random.choice(string.ascii_letters)
        conn.setblocking(0)
        data = random_string + "\n"
        conn.send(data.encode())  # send data to the client
        # # receive data stream. it won't accept data packet greater than 1024 bytes
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
            timeout_retries = 0
        else:
            result = "Timed out!\n"
            timeout_retries += 1
            conn.send(result.encode())

        if timeout_retries == 3:
            data = "Three continious retires over, game is now exiting\n Your score is %s" % score
            conn.send(data.encode())
            break

        if score == -3 or score == 10:
            data = "Game Over! Your score is %s\n" % score
            conn.send(data.encode())
            break

    conn.close()