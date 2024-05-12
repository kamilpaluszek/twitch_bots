import socket
import multiprocessing
import sys
import random
import time

# Twitch credentials for each account
ACCOUNTS = [
    {"NICK": "co_se_deje", "PASS": "oauth:bezu8gv9ssuaetzyyel8zd3x0j74l6"},
    {"NICK": "kocham_audice", "PASS": "oauth:nn9ezfrcvv559wmrqunr70v8tyqxvg"},
    {"NICK": "pomagacz_", "PASS": "oauth:2tzegzbkic8t1n9iebuao75ryuw7cr"},
    {"NICK": "nfs_mw_enjoyer", "PASS": "oauth:x4j8w3q9xf910w4fls020i19ae6wvt"},
    {"NICK": "przeszkadzacz", "PASS": "oauth:dbq7al72rl71wsb6w4eza91syrk33g"},
    {"NICK": "nazywamsiebloodwyn", "PASS": "oauth:u9sht39zvthjjllj87bcr05t7vbu1j"},
    {"NICK": "heavyliftenjoyer", "PASS": "oauth:aqs8jntxg63ydounam3w0hvkw0sxd9"},
    {"NICK": "tuskokracja", "PASS": "oauth:t5kfa3iu749a3ycwk1gxvfr2gq9a72"},
    {"NICK": "kochamzlom", "PASS": "oauth:e9euvs1unsw9r1tuwpze94xzqndfux"},
    {"NICK": "gothic3jestfajny", "PASS": "oauth:9ssrjqaa6a9jcjs2cn4tjxyy46dz7l"},
    {"NICK": "githic3toniegothic", "PASS": "oauth:gtoseh1on8bv8nff12srdlz1bdygi5"},
    {"NICK": "weebnumerouno", "PASS": "oauth:9pyox7lyn99c06d6r88p1umjs8eovz"},
    {"NICK": "bmw5istsenior", "PASS": "oauth:jq9wwyxfhx1rou3d6w3mz4sy0adhza"},
    {"NICK": "hinataloverforever69", "PASS": "oauth:ylts2do6rbaxjv95d7of562o4rl8pi"},
    {"NICK": "nfs_mw_enthusiast", "PASS": "oauth:e12ckusnnkxovradjo27pbhr79t02l"},
    {"NICK": "reliouzo_ty_gnido", "PASS": "oauth:qnxc63dfrxmosn1kaifnvip4gq7uom"},
    {"NICK": "Kushmon_Detailing", "PASS": "oauth:1b2pcf45ikja400scm3xtvdggct57y"},
    {"NICK": "kiedy_gotik", "PASS": "oauth:hxaowojqro72bvbv6708jjqqd8ssg9"},
    {"NICK": "Perla_Rojo_Rojewska", "PASS": "oauth:6mvqqf8es97hqimm0mnjh4jad6ehpx"},
    {"NICK": "Dobrze_Glosuje_PL", "PASS": "oauth:4znslxssv5k3war9816c38e87vlfax"},
    {"NICK": "Nienawidze_Dota2", "PASS": "oauth:nvkhudjlh3amjik7jov4dzo7rtj45i"},
    {"NICK": "mortadelka_enjoyer", "PASS": "oauth:j7wab1yxwp6hy2z1rluis82zohokak"},
    {"NICK": "zoladkowa_gorzka_mientowa", "PASS": "oauth:eni2gun89gvjuzw4rhqwt0cdcx9h0p"},
    {"NICK": "enkey_femboy", "PASS": "oauth:sr7489alk32uw3u4ua3lx26y0p1imr"},
    {"NICK": "enkey_nie_ma_nug", "PASS": "oauth:ormor018ia7w7o74c0ytvpf2322pdx"},

    {"NICK": "banujcie_relioso", "PASS": "oauth:wrwhagiaxi0lgeefottpvqex0osxvy"},
    {"NICK": "relioso_gnojuwa", "PASS": "oauth:vegu5335h9uvye0nove1s10b2i42h7"},
    {"NICK": "relioso_je_chrupioncom", "PASS": "oauth:nc1s0gflb3ytzq378wm4jud46ysmef"},
    {"NICK": "relioso_fan_mammona", "PASS": "oauth:iennjky4ev3kwdo3fa6hb3wa8rjy3e"},
    {"NICK": "relioso_to_ny9us", "PASS": "oauth:ones739c4p03j0vnzgp88tru1ha51i"},

    {"NICK": "Krajgo_20kg_deadlift", "PASS": "oauth:y3ewc6acpcu3dnbu6f8xv801ric9g5"},
    {"NICK": "Krajgo_kiedy_redukcja", "PASS": "oauth:cx78xpgpakjnkaoohhp8umay3zqbi3"},

    {"NICK": "weebnation_poe_noob", "PASS": "oauth:l83t0nvrniixnhohn1hn8hdqa3kx3d"},
    {"NICK": "weebnation_20iq_mod", "PASS": "oauth:ljqrd3599qtjgdbrzlcsxdv4g7amx4"},
    {"NICK": "poe_to_guwno", "PASS": "oauth:l6vlbxgherjcip7l4gfhbqhs3879bt"}
    ]
CHANNEL = "kebab_20cm"


def send_message(s, message):
    """
    Send a message to the specified channel.
    """
    message = "PRIVMSG #" + CHANNEL + " :" + message + "\r\n"
    time.sleep(0.4)
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
