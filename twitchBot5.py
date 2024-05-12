import socket
import multiprocessing
import sys
import random
import asyncio

# Twitch credentials for each account
ACCOUNTS = [
     {"NICK": "co_se_deje", "PASS": "oauth:bezu8gv9ssuaetzyyel8zd3x0j74l6"},
    {"NICK": "kocham_audice", "PASS": "oauth:nn9ezfrcvv559wmrqunr70v8tyqxvg"},
    {"NICK": "pomagacz_", "PASS": "oauth:2tzegzbkic8t1n9iebuao75ryuw7cr"},
    {"NICK": "nfs_mw_enjoyer", "PASS": "oauth:x4j8w3q9xf910w4fls020i19ae6wvt"},
    {"NICK": "przeszkadzacz", "PASS": "oauth:dbq7al72rl71wsb6w4eza91syrk33g"},
#    {"NICK": "nazywamsiebloodwyn", "PASS": "oauth:u9sht39zvthjjllj87bcr05t7vbu1j"},
#    {"NICK": "heavyliftenjoyer", "PASS": "oauth:aqs8jntxg63ydounam3w0hvkw0sxd9"},
#    {"NICK": "tuskokracja", "PASS": "oauth:t5kfa3iu749a3ycwk1gxvfr2gq9a72"},
#    {"NICK": "kochamzlom", "PASS": "oauth:e9euvs1unsw9r1tuwpze94xzqndfux"},
#    {"NICK": "gothic3jestfajny", "PASS": "oauth:9ssrjqaa6a9jcjs2cn4tjxyy46dz7l"},
#    {"NICK": "githic3toniegothic", "PASS": "oauth:gtoseh1on8bv8nff12srdlz1bdygi5"},
#    {"NICK": "weebnumerouno", "PASS": "oauth:9pyox7lyn99c06d6r88p1umjs8eovz"},
#    {"NICK": "bmw5istsenior", "PASS": "oauth:jq9wwyxfhx1rou3d6w3mz4sy0adhza"},
#    {"NICK": "hinataloverforever69", "PASS": "oauth:ylts2do6rbaxjv95d7of562o4rl8pi"},
#    {"NICK": "nfs_mw_enthusiast", "PASS": "oauth:e12ckusnnkxovradjo27pbhr79t02l"},
#    {"NICK": "reliouzo_ty_gnido", "PASS": "oauth:qnxc63dfrxmosn1kaifnvip4gq7uom"},
#    {"NICK": "Kushmon_Detailing", "PASS": "oauth:1b2pcf45ikja400scm3xtvdggct57y"},
#    {"NICK": "kiedy_gotik", "PASS": "oauth:hxaowojqro72bvbv6708jjqqd8ssg9"},
#    {"NICK": "Perla_Rojo_Rojewska", "PASS": "oauth:6mvqqf8es97hqimm0mnjh4jad6ehpx"},
#    {"NICK": "Dobrze_Glosuje_PL", "PASS": "oauth:4znslxssv5k3war9816c38e87vlfax"},
#    {"NICK": "Nienawidze_Dota2", "PASS": "oauth:nvkhudjlh3amjik7jov4dzo7rtj45i"},
#    {"NICK": "mortadelka_enjoyer", "PASS": "oauth:j7wab1yxwp6hy2z1rluis82zohokak"},
#    {"NICK": "zoladkowa_gorzka_mientowa", "PASS": "oauth:eni2gun89gvjuzw4rhqwt0cdcx9h0p"},
]

# Global channel
CHANNEL = "lodolamaczszymek"

async def send_message(nick, password, channel, message):
    """
    Send a message to the specified channel.
    """
    HOST = "irc.chat.twitch.tv"
    PORT = 6667

    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(f"PASS {password}\r\n".encode("utf-8"))
    s.send(f"NICK {nick}\r\n".encode("utf-8"))
    s.send(f"PRIVMSG #{channel} :{message}\r\n".encode("utf-8"))
    s.close()

async def receive_messages(nick, password):
    """
    Receive and process messages from the Twitch chat for a specific account.
    """
    HOST = "irc.chat.twitch.tv"
    PORT = 6667

    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(f"PASS {password}\r\n".encode("utf-8"))
    s.send(f"NICK {nick}\r\n".encode("utf-8"))

    while True:
        response = s.recv(2048).decode("utf-8")
        if "PING" in response:
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = response.split("!")[0][1:]
            message = ":".join(response.split(":")[2:])
            print(username + ": " + message)

async def send_messages(message):
    """
    Send a message from all accounts with random delays.
    """
    for account in ACCOUNTS:
        await asyncio.sleep(random.randint(1, 3))  # Random delay between 1 and 10 seconds
        await send_message(account["NICK"], account["PASS"], CHANNEL, message)

def start_receive_messages(nick, password):
    """
    Start receiving messages for a specific account.
    """
    asyncio.run(receive_messages(nick, password))

async def main():
    # Start receiving messages for each account using multiprocessing
    processes = []
    for account in ACCOUNTS:
        process = multiprocessing.Process(target=start_receive_messages, args=(account["NICK"], account["PASS"]))
        process.start()
        processes.append(process)

    # Main loop for sending messages from all accounts
    while True:
        message = input("Type your message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        else:
            await send_messages(message)

    # Terminate all processes
    for process in processes:
        process.terminate()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
