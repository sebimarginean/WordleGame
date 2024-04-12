import socket
import json
import colorama
import echo_protocol as echo

IP = '127.0.0.1'
PROMPT = 'Guess: '


def print_report(word, report):
    print(" " * len(PROMPT), end="")
    for i in range(len(report)):
        if report[i] == 'green':
            print(f'{colorama.Fore.GREEN}{word[i]}{colorama.Style.RESET_ALL}', end="")
        elif report[i] == 'yellow':
            print(f'{colorama.Fore.YELLOW}{word[i]}{colorama.Style.RESET_ALL}', end="")
        else:
            print(f'{word[i]}', end="")
    print()

if __name__ == "__main__":
    colorama.init()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, echo.PORT))

    socket_wrapper = echo.SocketWrapper(sock)

    print("Welcome to Wordle!")
    
    while True:
        data = socket_wrapper.recv_msg()
        data = json.loads(data)

        if data['type'] == 'start':
            number_of_underscores = data['value']
            underscores_string = "_" * number_of_underscores
            print(f"{PROMPT}{underscores_string}")

            while True:
                guess = input(PROMPT)
                guess_msg = json.dumps({'guess': guess})
                socket_wrapper.send_msg(guess_msg)
                response = socket_wrapper.recv_msg()
                response_data = json.loads(response)

                if response_data['type'] == 'bad_guess':
                    print('Bad guess, try again.')
                elif response_data['type'] == 'guessed':
                    print_report(guess, response_data['value'])
                    print("Well Done! You have guessed the word.")
                    break
                elif response_data['type'] == 'out_of_guesses':
                    print_report(guess, response_data['value'])
                    print("Out of guesses, the game will end.")
                    break
                elif response_data['type'] == 'report':
                    print_report(guess, response_data['value'])
                else:
                    print("Unknown message type received from server.")

            retry_data = socket_wrapper.recv_msg()
            retry_data_json = json.loads(retry_data)
            if retry_data_json['type'] == 'retry':
                retry_answer = input("Do you want to play again? (yes/no): ").strip().lower()
                socket_wrapper.send_msg(retry_answer)
                
                if retry_answer != 'yes':
                    break

    print("Thanks for playing. Goodbye!")

