import socket
import threading
import time
import random
from ascii_color import *

print(Tc.Fg.LIGHTBLUE+"[STARTUP] Initializing ..."+Tc.RESET)
beginning = time.time()

PORT = 5050
ADRESS = socket.gethostbyname(socket.gethostname())
VERSION = "0.0"
FORMAT = "utf-8"
usernames = {} #store usernames and the id of the room they are in {"username": {"room": "room_id", object: obj}}
rooms = {} #store Room objects {"room_name": obj}
connect_threads = []
message_threads = []
room_thrads = []

class Room():
    """
    creates a new chat room
    """
    # print(Tc.Fg.CYAN+"[ROOM",str(self.__id)+"-"+self.__name+"]"+Tc.RESET)

    def __init__(self, name):
        self.__members = {}
        self.__messages = []
        self.__id = random.randint(0, 32767)
        self.__name = name
        print(Tc.Fg.CYAN+"[ROOM",str(self.__id)+"-"+self.__name+"] new room got created"+Tc.RESET)
    
    def new_member(self, username:str, conn:socket.socket, adrr:tuple, overrride:bool = False):
        if username in self.__members:
            if overrride:
                self.__members[username] = (conn, adrr)
        else:
            self.__members[username] = (conn, adrr)
        print(Tc.Fg.CYAN+"[ROOM",str(self.__id)+"-"+self.__name+"] added member",username,"to the room"+Tc.RESET)

    def remove_member(self, username:str) -> bool:
        try:
            del self.__members[username]
        except:
            return False
        else:
            print(Tc.Fg.CYAN+"[ROOM",str(self.__id)+"-"+self.__name+"] removed",username,"from the room"+Tc.RESET)
            return True

    def get_members(self) -> dict:
        return list(self.__members.keys())
    
    def get_stats(self) -> str:
        string = Tc.Fg.CYAN
        string += "Information about the Room " + str(self.__id) + ":\n"
        string += "Member count: " + str(len(self.__members)) + "\n"
        string += "Members: " 
        members = self.get_members()
        for i in range(10):
            try:
                username = members[i]
            except:
                pass
            else:
                string += username + ", "
        if len(members) > 10:
            string += "...\n"
        else:
            string += "\n"
        string += "Total messages: " + str(len(self.__messages))
        string += Tc.RESET
        return string
    
    def recieved_message(self, message:str, sender:str):
        print(Tc.Fg.CYAN+"[ROOM",str(self.__id)+"-"+self.__name+"] got message", message, "from", sender + Tc.RESET)
        self.__messages.append({sender: message})
        try:
            for user in self.__members:
                #if user != sender:
                self.__members[user][0].send(("["+sender+"] "+message).encode(FORMAT))
        except:
            print(Tc.Fg.CYAN+"[ROOM",str(self.__id)+"-"+self.__name+"] error occured while sending message to members"+Tc.RESET)

def listen_for_connections(limit:int = 0) -> object:
    interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            interface.bind((ADRESS, PORT))
        except OSError:
            print(Tc.Fg.RED+"[CONNECTION LISTENER] Host adress allready in use, trying again in 30 sec")
            time.sleep(30)
        else:
            break
    interface.listen(limit)
    print(Tc.Fg.PURPLE+"[CONNECTION LISTENER] started."+Tc.RESET)
    while True:
        connection_id = random.randint(0, 65535)
        conn, adrr = interface.accept()
        print(Tc.Fg.PURPLE+"[CONNECTION LISTENER",str(connection_id)+"] catched connection with adress", str(adrr[0]),"at port", str(adrr[1])+Tc.RESET)
        connect_threads.append(threading.Thread(target=connect_new_user, args=(connection_id, conn, adrr), name="connector-"+str(connection_id)))
        connect_threads[-1].start()

def connect_new_user(connection_id, conn:socket.socket, adrr):
    try:
        version_ok = False
        username_ok = False
        room_ok = False

        while True:
            if not version_ok:
                conn.send("get_version".encode(FORMAT))
                if conn.recv(2048).decode(FORMAT) == VERSION:
                    conn.send("version_ok".encode(FORMAT))
                    version_ok = True
                    #print("Version ok")
                else:
                    conn.send("version_not_ok".encode(FORMAT))
                    conn.send(VERSION.encode(FORMAT))
                    conn.close()
            time.sleep(0.1)
            if version_ok and not username_ok:
                conn.send("get_username".encode(FORMAT))
                username = conn.recv(2048).decode(FORMAT)
                if not username in list(usernames.keys()):
                    conn.send("username_ok".encode(FORMAT))
                    username_ok = True
                    #print("username", username, "ok")
                else:
                    conn.send("username_not_ok".encode(FORMAT))
            time.sleep(0.1)
            if version_ok and username_ok and not room_ok:
                conn.send("get_room".encode(FORMAT))
                room_name = conn.recv(2048).decode(FORMAT)
                if room_name in list(rooms.keys()):
                    conn.send("room_ok".encode(FORMAT))
                    room_ok = True
                    #print("room", room_name, "ok")
                else:
                    conn.send("room_not_ok".encode(FORMAT))
                    if conn.recv(2048).decode(FORMAT) == "y":
                        rooms[room_name] = Room(room_name)
                        room_ok = True
            time.sleep(0.1)
            if version_ok and username_ok and room_ok:
                rooms[room_name].new_member(username, conn, adrr)
                # print(rooms[room_name].get_stats())
                usernames[username] = {"room": room_name, "object": conn}
                conn.send("handshake_ok".encode(FORMAT))
                message_threads.append(threading.Thread(target=message_listener, args=(conn, username, room_name), name="message-listener-"+username))
                message_threads[-1].start()
                break
    except:
        print(Tc.Fg.PURPLE+"[CONNECTION LISTENER "+str(connection_id)+"]", "disconnected during handshake process"+Tc.RESET)
    connect_threads.remove(threading.current_thread())
    print(Tc.Fg.PURPLE+"[CONNECTION LISTENER "+str(connection_id)+"]", "done"+Tc.RESET)

def console_manager():
    print(Tc.Fg.DARKGREY+"[CONSOLE MANAGER] got started.")
    while True:
        string = Tc.Fg.DARKGREY
        command = input().split()
        try:
            all = False
            debug = False
            if command[1] == "-all":
                all = True
            elif command[1] == "-debug":
                debug = True
        except:
            pass
        
        if command[0] == "/help":
            string += "Commands for the chat.py server:\n"
            string += "/help: brings up this command overview message\n"
            string += "/rooms: lists 10 objects, if -all argument provided it will show all rooms (might take a while)\n"
            string += "/members: lists 20 users, if -all argument provided it will show all users (might take a while)\n"
            string += "/threads: lists 10 active threads, if -debug argument provided it will show a list with all threads (might take a while)\n"
            string += "/quit: shutdown the server (it is just quit()) WIP"

        elif command[0] == "/rooms":
            string += "Current Rooms ("+str(len(list(rooms.keys())))+"):\n"
            if len(list(rooms.keys())) == 0:
                string += "no active rooms"
            elif len(list(rooms.keys())) > 10 and all:
                i = 0
                for room in rooms:
                    string += "- " + room + " (" +str(len(list(rooms.values())[i].get_members())) + ")\n"
                    i += 1
            else:
                i = 0
                while i < 10:
                    try:
                        string += "- " + list(rooms.keys())[i] + " (" +str(len(list(rooms.values())[i].get_members())) + ")\n"
                    except:
                        break
                    else:
                        i += 1
            if debug:
                string += str(rooms)

        # elif command[0] == "/room":
        #     try:
        #             string += rooms[command[1]].get_stats()
        #     except:
        #         string += "Room", command[1], "does not exist"

        elif command[0] == "/members":
            string += "Current Members ("+str(len(list(usernames.keys())))+"):\n"
            if len(list(rooms.keys())) == 0:
                string += "no active members"
            elif len(list(rooms.keys())) > 10 and all:
                for member in usernames:
                    string += "- " + member + " ("+  +")\n"
            else:
                i = 0
                while i < 20:
                    try:
                        string += "- " + list(usernames.keys())[i] + "\n"
                    except:
                        break
                    else:
                        i += 1
            if debug:
                string += str(usernames)
        
        elif command[0] == "/threads":
            string += "Current active threads ("+str(threading.active_count())+"):\n"
            string += "Active connection threads: " + str(len(connect_threads)) + "\n"
            string += "Acrive user listener: " + str(len(message_threads)) + "\n"
            string += "Active room threads: " + str(len(room_thrads)) + "\n"
            if debug:
                string += str(threading.enumerate()) + "\n"
                string += str(connect_threads) + "\n"
                string += str(message_threads) + "\n"
                string += str(room_thrads)

        elif command[0] == "/quit":
            string = Tc.Fg.RED
            string += "[SHUTDOWN] Shutting down the server ..."
            string += Tc.RESET
            print(string)

        else:
            string += "This command does not exist, use /help to show you a list of all commands"
        string = string.strip("\n")
        string += Tc.RESET
        print(string)

def message_listener(usr_obj:socket.socket, username:str, user_room:str):
    #{"username": {"room": "room_id", object: obj}}
    print(Tc.Fg.PURPLE+"[MESSAGE LISTENER] for", username, "in room", user_room, "started"+Tc.RESET)
    while True:
        try:
            data = usr_obj.recv(2048)
        except:
            break
        if not data:
            break
        else:
            rooms[user_room].recieved_message(data.decode(FORMAT), username)
    print(Tc.Fg.PURPLE+"[MESSAGE LISTENER] user", username, "disconnected"+Tc.RESET)
    rooms[user_room].remove_member(username)
    usernames.pop(username)
    message_threads.remove(threading.current_thread())

print(Tc.Fg.LIGHTGREEN+"[STARTUP] Initialized in", str(round(time.time()-beginning, 5)),"sec"+Tc.RESET)
print(Tc.Fg.LIGHTBLUE+"[STARTUP] Starting Server ..."+Tc.RESET)
beginning = time.time()
console = threading.Thread(target=console_manager, name="console-manager")
console.start()
connection_listener = threading.Thread(target=listen_for_connections, name="connection-listener")
connection_listener.start()
print(Tc.Fg.LIGHTGREEN+"[STARTUP] Server started in", str(round(time.time()-beginning, 5)),"sec"+Tc.RESET)