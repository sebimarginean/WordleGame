# Wordle Game

## Description

This project implements a simple version of the popular word guessing game, Wordle, utilizing Python's socket programming for network communication. It is structured into three main components: an echo protocol, a Wordle client, and a Wordle server, showcasing the use of sockets for enabling real-time communication between the client and server.

## Components

### Echo Protocol (`echo_protocol.py`)

- A foundational element that employs socket programming for testing network communication. It demonstrates sending a message from the client to the server and receiving an echoed response, laying the groundwork for the project's communication mechanism.

### Wordle Client (`wordle_client.py`)

- The client-side application where users interact with the game. It sends guesses to the server through a socket connection and displays feedback based on the server's response.

### Wordle Server (`wordle_server.py`)

- Manages the game's logic and processes guesses received from the client over a socket connection. It evaluates the guesses against the target word and returns feedback to guide the player towards the correct answer.


## Usage

After initiating the server and the client:

1. The client prompts you to enter your guess for the word of the day.

2. Submit your guess; the server processes it and returns feedback through the socket connection.

3. Utilize the feedback to make informed guesses within the allowed attempts.

4. The game ends when you correctly guess the word or use up all your attempts.

## Technical Details

- This project leverages Python's socket programming to facilitate communication between the client and server, ensuring real-time interaction and feedback during the game.

- The echo protocol serves as a basic demonstration of this communication, while the Wordle game extends this to a practical application, handling guess evaluations and session management.

- The use of TCP/IP sockets ensures reliable data transmission and connection management between the client and server.

## Contributing

Contributions are welcome. Please fork the repository, make your changes, and submit a pull request for review.

## License

The project is open-source, under the MIT License. See the LICENSE file for more details.
