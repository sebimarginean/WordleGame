import socket
import threading
import json
import requests
import random
import echo_protocol as echo
 
IP = '127.0.0.1'

def create_report(expected, actual):
    report = ["none" for _ in range(len(expected))]
    for i in range(len(expected)):
        if expected[i] == actual[i]:
            report[i] = "green"
        elif actual[i] in expected:
            report[i] = "yellow"
    return report


def create_bad_guess_msg():
    return json.dumps({'type': 'bad_guess'})

def create_guessed_msg(expected, actual):
    return json.dumps({'type': 'guessed', 'value': create_report(expected, actual)})

def create_report_msg(expected, actual):
    return json.dumps({'type': 'report', 'value': create_report(expected, actual)})

def create_out_of_guesses_msg(expected, actual):
    return json.dumps({'type': 'out_of_guesses', 'value': create_report(expected, actual)})

def handle_client(client_socket, client_address):
    print(f"Thread for handling client: {client_address}")
    sock_wrapper = echo.SocketWrapper(client_socket)

    response = requests.get("https://www.mit.edu/~ecprice/wordlist.10000").content
    words_list = response.decode("utf-8").split("\n")

    while True:
        guesses = 0
        max_guesses = 6
        word = words_list[random.randint(0, len(words_list)-1)]

        sock_wrapper.send_msg(json.dumps({'type': 'start', 'value': len(word)}))

        while True:
            msg = sock_wrapper.recv_msg()
            if not msg:
                print("Unexpected game exit.")
                break

            msg = json.loads(msg)
            guess = msg.get('guess')
            if guess:
                guesses += 1

                if len(guess) != len(word):
                    bad_guess = create_bad_guess_msg()
                    sock_wrapper.send_msg(bad_guess)
                elif guess == word:
                    guessed = create_guessed_msg(word, guess)
                    sock_wrapper.send_msg(guessed)
                    break
                elif guesses == max_guesses:
                    out_of_guesses = create_out_of_guesses_msg(word, guess)
                    sock_wrapper.send_msg(out_of_guesses)
                    break
                else:
                    report = create_report_msg(word, guess)
                    sock_wrapper.send_msg(report)
            else:
                continue

        retry_msg = {'type': 'retry'}
        sock_wrapper.send_msg(json.dumps(retry_msg))
        retry_response = sock_wrapper.recv_msg()
        if retry_response.lower() != 'yes':
            break

    print(f"Done with client {client_address}")

if __name__ == "__main__":
    print("Welcome to Wordle Server!")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, echo.PORT))
    sock.listen()
    while True:
        print("Ready to accept a client connection.")
        client_sock, addr = sock.accept()
        print(f"Accepted new client connection: {addr}")
        th = threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True)
        th.start()
