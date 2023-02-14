import random
import socket
import time
import threading

class Tc:
    '''Colors class:
    Reset all colors with colors.reset
    Two subclasses fg for foreground and bg for background.
    Use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    Also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold
    '''
    RESET='\033[0m'
    BOLD='\033[01m'
    DISABLE='\033[02m'
    UNDERLINE='\033[04m'
    REVERSE='\033[07m'
    STRIKETHROUGH='\033[09m'
    INVISIBLE='\033[08m'
    ITALIC='\33[3m'
    class Fg:
        BLACK='\033[30m'
        RED='\033[31m'
        GREEN='\033[32m'
        BLUE='\033[34m'
        PURPLE='\033[35m'
        CYAN='\033[36m'
        LIGHTGREY='\033[37m'
        DARKGREY='\033[90m'
        LIGHTRED='\033[91m'
        LIGHTGREEN='\033[92m'
        YELLOW='\033[93m'
        LIGHTBLUE='\033[94m'
        PINK='\033[95m'
        LIGHTCYAN='\033[96m'
    class Bg:
        BLACK='\033[40m'
        RED='\033[41m'
        GREEN='\033[42m'
        YELLOW='\033[43m'
        BLUE='\033[44m'
        PURPLE='\033[45m'
        CYAN='\033[46m'
        LIGHTGREY='\033[47m'

print(Tc.Fg.LIGHTBLUE+"[STARTUP] Client stated!"+Tc.RESET)

interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_ADRR = "192.168.178.18"
PORT = 5050
VERSION = "0.0"
FORMAT = "utf-8"

while True:
    try:
        interface.connect((IP_ADRR, PORT))
    except:
        print(Tc.Fg.RED+"[STARTUP] Could not connect to server, retrying in 10 sec"+Tc.RESET)
        time.sleep(10)
    else:
        try:
            print(Tc.Fg.LIGHTBLUE+"[STARTUP] Connection established, starting handshake process ..."+Tc.RESET)
            version_ok = False
            username_ok = False
            room_ok = False
            while True:
                req = interface.recv(2048).decode(FORMAT)
                if req == "get_version":
                    interface.send(VERSION.encode(FORMAT))
                elif req == "version_ok":
                    print(Tc.Fg.LIGHTGREEN+"Client version ok"+Tc.RESET)
                elif req == "version_not_ok":
                    print(Tc.Fg.RED+"Version outdated, client version:", VERSION, "server version:", interface.recv(2048).decode(FORMAT)+Tc.RESET)
                    interface.close()
                    quit()
                elif req == "get_username":
                    interface.send(input(Tc.Fg.YELLOW+"Enter username: "+Tc.RESET).encode(FORMAT))
                    #interface.send(str(random.randint(0, 10)).encode(FORMAT))
                elif req == "username_ok":
                    print(Tc.Fg.LIGHTGREEN+"Username ok"+Tc.RESET)
                elif req == "username_not_ok":
                    print(Tc.Fg.RED+"Username allready taken"+Tc.RESET)
                elif req == "get_room":
                    interface.send(input(Tc.Fg.YELLOW+"Enter Room name: "+Tc.RESET).encode(FORMAT))
                    #interface.send("Discord".encode(FORMAT))
                elif req == "room_ok":
                    print(Tc.Fg.LIGHTGREEN+"Room ok"+Tc.RESET)
                elif req == "room_not_ok":
                    print(Tc.Fg.RED+"Room does not exist"+Tc.RESET)
                    interface.send(input(Tc.Fg.YELLOW+"Would you like to create it? [y/n] "+Tc.RESET).encode(FORMAT))
                    #interface.send("y".encode(FORMAT))
                elif req == "handshake_ok":
                    print(Tc.Fg.GREEN+"[STARTUP] Handshake process successful."+Tc.RESET)
                    break
                else:
                    print(req)
        except:
            print(Tc.Fg.LIGHTBLUE+"[STARTUP] Lost connection to server during startup"+Tc.RESET)
        break

def recieve():
    print(Tc.Fg.CYAN+"[MESSAGE RECIEVER] started"+Tc.RESET)
    while True:
        data = interface.recv(2048)
        if not data:
            break
        else:
            print(data.decode(FORMAT))
    print(Tc.Fg.CYAN+"[MESSAGE RECIEVER] quit"+Tc.RESET)

reciever = threading.Thread(target=recieve)
reciever.start()

while True:
    interface.send(input().encode(FORMAT))