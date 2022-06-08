# implementing 3-tier structure: Hall --> Room --> Clients; 

import select, sys
from pychat_util import Hall, User
import pychat_util

READ_BUFFER = 4096

ip_address = sys.argv[1] if len(sys.argv) >= 2 else ''
#sys.argv to read input from command line
#python3 pychat_server.py ipadd returns sys.argv as [pychat_server.py, ipadd] => len = 2
#ip_address = 1st element

#creates socket to listen to the port using the 'ip_address'
listen_sock = pychat_util.create_socket((ip_address, pychat_util.PORT))

#creates a Hall object
hall = Hall()

#adds the created socket to the connected sockets list
connection_list = []
connection_list.append(listen_sock)

while True:
    # every user is a socket
    # select finds the status of file descriptors - read, write and error
    # --------------- doubt ------------

    read_users, write_users, error_sockets = select.select(connection_list, [], [])
    for user in read_users:
        if user is listen_sock: 
            # new user
            new_socket, add = user.accept()

            # create a new socket, ie user
            new_user = User(new_socket)
            # add the new user to the connection list
            connection_list.append(new_user)
            # print welcome msg
            hall.welcome_new(new_user)

        else:
            msg = user.socket.recv(READ_BUFFER)
            if msg:
                msg = msg.decode().lower()
                hall.handle_msg(user, msg)
            else:
                user.socket.close()
                connection_list.remove(user)

    for sock in error_sockets: # close error sockets
        sock.close()
        connection_list.remove(sock)
