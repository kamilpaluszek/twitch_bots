import socket


# Twitch credentials
HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "kocham_audice"
PASS = "oauth:nn9ezfrcvv559wmrqunr70v8tyqxvg"
CHANNEL = "eold"

def send_message(s, message):
    """
    Send a message to the specified channel.
    """
    message = "PRIVMSG #" + CHANNEL + " :" + message + "\r\n"
    s.send(message.encode("utf-8"))

def receive_messages():
    """
    Receive and process messages from the Twitch chat.
    """
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(CHANNEL).encode("utf-8"))

    while True:
#        resp = s.recv(2048).decode('utf-8')
#
#        if resp.startswith('PING'):
#            s.send("PONG\n".encode('utf-8'))
#    
#        elif len(resp) > 0:
#            print(resp)
        response = s.recv(2048).decode("utf-8")
        print(response)
        if "PING" in response:
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = response.split("!")[0][1:]
            message = ":".join(response.split(":")[2:])
            print(username + ": " + message)

            # Check if message is from a specific user
            if username.lower() == "wir_wydarzen":
                # Send a response message
                send_message(s, "Hello")

if __name__ == "__main__":
    receive_messages()
