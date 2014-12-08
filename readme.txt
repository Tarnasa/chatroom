* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

  Coded by: Luke Simon and Joshua Wyss
  Class: CS 3800
  Professors: Dr. Ercal and Dr. Chellappan
  File Purpose: Describing how to run and use our chatroom

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

We use the python language version 2.7.6 (current version on 
the cs linux machines)

=== To Run Our Chatroom
Assumption: you are connected to a single cs linux machine and 
already navigated to the directory containing the files.

1. Type "python server.py" to start our server (no further
    input required until shutdown)
2. In a new window type "python client.py" to start a client
3. Client asks for host name.
    Type the host name provided in the server window between the
    tick marks. Example: '131.121.31.2' or 'rc02xcs213.managed.mst.edu'
4. Client asks for port number.
    Type the port number provided in the server window after
    the host name. Example: 49152
5. Client asks for user name.
    Provide a unique user name not previously used, unless you want
    to test our user name check. :D
    Example: lizzy
6. You can now send messages to the server, which are also sent
    to other clients if they are connected.
7. Repeat steps 2-6 for each new client, up to 10 of them.
8. Have conversations
9. Shutdown the server with ctrl-c.
    -or- Shutdown each individual client with one of the following:
            '/quit', '/part', '/exit'
