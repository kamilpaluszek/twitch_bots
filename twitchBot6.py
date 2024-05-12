import openai
import socket
import time
import random

openai.api_key = "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"

CHANNEL = "lodolamaczszymek"
NICK = "wkurwiony_zaruwa"
PASS = "oauth:r2qfn5qigsj9l7320hkblnzadoxz3y"


#check if bot and user exchanged 8 messages, if yes then delete list[1] and list[2]
def checkmsg(list):
  if(len(list) > 20):
    del list[1:3]
  return list

def send_message(message, responder):
    """
    Send a message to the specified channel.
    """
    HOST = "irc.chat.twitch.tv"
    PORT = 6667

    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(CHANNEL).encode("utf-8"))

    message = "PRIVMSG #" + CHANNEL + " :" + "@" + responder + " " + message + "\r\n"
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
        message = ":".join(response.split(":")[2:])
        print(message)
        if "@" + NICK in message:
            username = response.split("!")[0][1:]
            print("Wiadomosc napisal user: " +username)
            # print("OFIARA NAPISALA XD")
            #message = ":".join(response.split(":")[2:])
            print("RESPONDER NAPISAL: " + message)
            return message, username


def chatbot():
  # Create a list to store all the messages for context
  messages = [
    {"role": "system", "content": "You are angry person that is insulting every person that talks to you. You are very mean to everyone for no reason. You can swear and answer questions in mean way. You're only using Polish language. Your messages are in 2 or 3 sentences max."},
  ]
  #send_message("Ale ta dota2 to hujnia")
  # Keep repeating the following
  while True:
    message, username = receive_messages(NICK, PASS)
    print("chatbot message, username:" + message, username)
    time.sleep(random.randint(3, 12))
    # Add each new message to the list
    messages.append({"role": "user", "content": message})

    # Request gpt-3.5-turbo for chat completion
    response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages,
      temperature=0.7,
    )

    # Print the response and add it to the messages list
    chat_message = response.choices[0].message.content
    #Send response from chatgpt to CHANNEL
    send_message(chat_message, username)
    messages.append({"role": "assistant", "content": chat_message})
    checkmsg(messages)


if __name__ == "__main__":
    chatbot()
