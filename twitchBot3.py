import socket
import multiprocessing
import sys
import random
import time

# Twitch credentials for each account
ACCOUNTS = [
    {"NICK": "kocham_audice", "PASS": "oauth:nn9ezfrcvv559wmrqunr70v8tyqxvg"},
    {"NICK": "pomagacz_", "PASS": "oauth:2tzegzbkic8t1n9iebuao75ryuw7cr"},
#    {"NICK": "nfs_mw_enjoyer", "PASS": "oauth:x4j8w3q9xf910w4fls020i19ae6wvt"},
#    {"NICK": "przeszkadzacz", "PASS": "oauth:yu088ivvgb6qxp9rc4toym3369l7ke"},
]
CHANNEL = "mg_quanlon"


def send_message(s, message):
    """
    Send a message to the specified channel.
    """
    message = "PRIVMSG #" + CHANNEL + " :" + message + "\r\n"
    s.send(message.encode("utf-8"))

def receive_messages(NICK, PASS):
    """
    Receive and process messages from the Twitch chat for a specific account.
    """
    HOST = "irc.chat.twitch.tv"
    PORT = 6667

    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(CHANNEL).encode("utf-8"))

    while True:
        response = s.recv(2048).decode("utf-8")
        if "PING" in response:
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = response.split("!")[0][1:]
            message = ":".join(response.split(":")[2:])
            print(username + ": " + message)

def send_messages(message):
    """
    Send a message from all accounts.
    """
    for account in ACCOUNTS:
        HOST = "irc.chat.twitch.tv"
        PORT = 6667

        s = socket.socket()
        s.connect((HOST, PORT))
        s.send("PASS {}\r\n".format(account["PASS"]).encode("utf-8"))
        s.send("NICK {}\r\n".format(account["NICK"]).encode("utf-8"))
        s.send("JOIN #{}\r\n".format(CHANNEL).encode("utf-8"))

        send_message(s, message)

if __name__ == "__main__":
    processes = []

    for account in ACCOUNTS:
        process = multiprocessing.Process(target=receive_messages, args=(account["NICK"], account["PASS"]))
        processes.append(process)
        process.start()

    # Main loop for sending messages from all accounts
    while True:
        message = input("Type your message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        else:
            send_messages(message)
    
    # Terminate all processes
    for process in processes:
        process.terminate()

    sys.exit(0)
