# implementing 3-tier structure: Hall --> Room --> Clients;
from termcolor import colored
import socket

MAX_CLIENTS = 30
PORT = 22222
QUIT_STRING = '<$quit$>'


def create_socket(address):
    # AF_INET: address family of internet
    # SOCK_STREAM: by def: TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # allows to resuse address
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    # binds address to socket
    s.bind(address)
    # listens to a max of 30 clients
    s.listen(MAX_CLIENTS)
    print(colored(f"Now listening at {(str(address))}", 'blue'))
    return s


class Hall:
    def __init__(self):
        # dictionary having room_name and the Room object as k:v pair
        self.rooms = {}

        # dictionary having user_name and the room_name as k:v pair - to see to which room the user belongs to
        self.user_room_map = {}

    def welcome_new(self, new_user):
        new_user.socket.sendall(
            b'Welcome to chattie.\nPlease tell us your name:\n')

    def list_rooms(self, user):

        if len(self.rooms) == 0:
            msg = 'Oops, no rooms are active currently.\n' \
                + 'Use [!join room_name] to create a new room.\n'
            user.socket.sendall(msg.encode())
        else:
            msg = 'Active rooms:\n'
            # print details and users of every room
            for room in self.rooms:
                msg += room + ": " + \
                    str(len(self.rooms[room].users)) + " user(s)\n"
            user.socket.sendall(msg.encode())

    def handle_msg(self, user, msg):

        instructions = b'\nInstructions:\n'\
            + b'[!show] to list all rooms\n'\
            + b'[!join room_name] to join/create/switch to a room\n' \
            + b'[!man] to show instructions\n' \
            + b'[!q] to quit\n' \
            + b'Otherwise start typing and enjoy!\n' \
            + b'\n'

        print(colored(user.name, 'yellow') + " > " + msg)

        # new connection
        if "name:" in msg:
            user.name = msg.split()[1]
            print(colored(f"New connection from: {user.name}", 'green'))
            user.socket.sendall(instructions)

        elif "!join" in msg:
            same_room = False
            if len(msg.split()) >= 2:  # error check
                room_name = msg.split()[1]

                # if user in the dict already
                if user.name in self.user_room_map:
                    # if the input room is same as the room in which user is there,
                    if self.user_room_map[user.name] == room_name:
                        user.socket.sendall(
                            b'You are already in room: ' + room_name.encode())
                        same_room = True
                    else:  # switch
                        old_room = self.user_room_map[user.name]

                        # removes the user from the old room
                        self.rooms[old_room].remove_user(user)
                
                if not same_room:
                    # if the room does not exist yet, create a new Room object
                    if not room_name in self.rooms:
                        new_room = Room(room_name)
                        # assign the ROom object to the room_name in the dict
                        self.rooms[room_name] = new_room

                    # add the user to the room
                    self.rooms[room_name].users.append(user)

                    # welcomes user
                    self.rooms[room_name].welcome_new(user)

                    # assigns this user to the new room
                    self.user_room_map[user.name] = room_name
            else:
                user.socket.sendall(instructions)

        elif "!show" in msg:
            self.list_rooms(user)

        elif "!man" in msg:
            user.socket.sendall(instructions)

        elif "!q" in msg:
            user.socket.sendall(QUIT_STRING.encode())
            self.remove_user(user)

        else:
            # check if in a room or not first
            if user.name in self.user_room_map:
                self.rooms[self.user_room_map[user.name]
                           ].broadcast(user, msg.encode())
            else:
                # a person can chat publicly without joining a room
                msg = 'Join a room to chat \n' \
                    + 'Use [!show] to see available rooms! \n' \
                    + 'Use [!join room_name] to join a room! \n'
                user.socket.sendall(msg.encode())

    def remove_user(self, user):
        if user.name in self.user_room_map:
            self.rooms[self.user_room_map[user.name]].remove_user(user)
            del self.user_room_map[user.name]
        print(colored(f'{user.name} has left the chat', 'red'))


class Room:
    def __init__(self, name):
        self.users = []  # a list of sockets (i.e., users)
        self.name = name  # room name

    def broadcast(self, from_user, msg):
        # prints( user: msg)
        msg = from_user.name.encode() + b" : " + msg

        # sends the msg to every one in the room
        for user in self.users:
            user.socket.sendall(msg)

    def welcome_new(self, from_user):
        msg = from_user.name + " joins "+self.name + '\n'
        for user in self.users:
            user.socket.sendall(msg.encode())

    def remove_user(self, user):
        self.users.remove(user)
        leave_msg = user.name.encode() + b" has left the room\n"
        self.broadcast(user, leave_msg)


class User:
    # gives name as "new" by default
    def __init__(self, socket, name="new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name

    # returns file descriptor
    def fileno(self):
        return self.socket.fileno()
