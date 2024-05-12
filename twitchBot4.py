import openai
import socket
import random
import time

openai.api_key = "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"

ACCOUNTS = [{"NICK": "weebnation_20iq_mod", "PASS": "oauth:ljqrd3599qtjgdbrzlcsxdv4g7amx4"}
    ]

CHANNEL = "karina7kotova"
NICK = "weebnation_20iq_mod"
PASS = "oauth:ljqrd3599qtjgdbrzlcsxdv4g7amx4"
OFIARA = "nfs_mw_enjoyer"


#check if bot and user exchanged 8 messages, if yes then delete list[1] and list[2]
def checkmsg(list):
  if(len(list) > 20):
    del list[1:3]
  return list

def send_message(message):
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

    message = "PRIVMSG #" + CHANNEL + " :" + "@" + OFIARA + " " + message + "\r\n"
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
        if(username.strip() == OFIARA):
            # print("OFIARA NAPISALA XD")
            message = ":".join(response.split(":")[2:])
            print("OFIARA NAPISALA: " + message)
            return message


def chatbot():
  # Create a list to store all the messages for context
  messages = [
    {"role": "system", "content": "You are positive person asking questions about a lot of topics, mainly what happens in the world, in Polish language, in maximum 2 sentences."},
  ]
  
  # Keep repeating the following
  while True:
    message = receive_messages(NICK, PASS)

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
    time.sleep(random.randint(10, 30))
    send_message(chat_message)
    messages.append({"role": "assistant", "content": chat_message})
    checkmsg(messages)


if __name__ == "__main__":
    chatbot()
