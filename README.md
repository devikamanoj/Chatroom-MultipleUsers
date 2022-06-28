# CHATROOM WITH MULTIPLE USERS

Chatroom with multiple users provides an user to chat with all the members in the specific room they are in and not with other members in other rooms. Other than the users, these messages are visible to the server. Using the concept of socket programming we have developed this chatroom. Here, we use python language to create a chatroom with multiple users

## CLIENT - SERVER APPLICATION

Client server mode is an information sharing mode which is used widely in information system. The client usually refers to PC or workstation and it provides the terminal client with very friendly interface. The database server is the most common one, it makes many client share the same access to sources of information.

## IMPLEMENTATION


### Server.py
Reads and validates the IP address of server from the command line and creates an opening socket to listen if any clients connect. A new Hall is created for users to chat. Initially the Hall has no rooms in it. Whenever a new user comes they are added to hall. Once a user joins, server rolls out the user manual and continues listening to the clients. A check for error sockets are also done, which is then closed and removed.

### Client.py

Creates a client. The client gets connected to the IP address mentioned in the commandline after validating. If the server is not up, or if the command is invalid, the program exits.
Once the client is successfully connected to the server, the name is asked, and is welcomed to the Hall. 

### Class Hall
Hall is the landing area for all the users. The Hall class has two dictionaries: one that maps room name and the Room object, and another that maps a user and the room in which they belong to.
A hall can have multiple rooms which is stored in the dictionary along with Room instances. 
This class handles:

    - welcoming a new user to the Hall
    - listing all the rooms
    - printing the instruction manual
    - joining the user to a room
    - handles the user commands like join, list, quit etc
    - Has all the details about all the rooms present.
    
### Class Room

Room class has two fields: a list to store users in a room, and the corresponding room name. Room is a private space where users in that room can talk to each other. No one in the hall, or in other groups can be part of that conversation. This class handles all the user commands related to Room like joining, listing rooms, leaving etc.

### Class User

In this project, every User is simply a socket. We create a socket for every new player, and connects it with the server. A user is named as "new" by default, and the user can change it when prompted. This class returns a file descriptor for the user.

## How to Use

* Install the python 3 version
* Download and unzip all the above files


* To fire up server:
```python
python3 pychat_server.py [host]
```

* To fire up client:
```python
python3 pychat_client.py host
```
