#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import thread
import os
import time
import subprocess
import sys

myMap = {
    "camara on" : "ps > /tmp/ps.lst",
    "fuego on" : "df",
    "sleep" : "sleep 10 ; echo 'hi'"
}



def on_new_client(clientsocket,addr):
    while True:
        try: 
            msg = clientsocket.recv(1024)
        except:
            break

        print ' Rec ', msg

        cmd=myMap.get(msg)
        if cmd:
            try:
                print cmd
                process = subprocess.Popen(cmd.split())
                # process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
                #output, error = process.communicate()
                #print output
                #print error
                response = "exec"
            except:
                print sys.exc_info()[0]
                response = "failed"
        else:
            response = "not found"

        #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
        print response
        try:
            clientsocket.send(response)
        except:
            break

    clientsocket.close()








#s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
#port = 50000                # Reserve a port for your service.


s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

try:
    os.remove("/tmp/channel0")
except OSError:
    pass



#print 'Server started!'
#thread.start_new_thread(serialServer,())


print 'Waiting for clients...'

s.bind("/tmp/channel0")
#s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

#print 'Got connection from', addr
while True:
    c, addr = s.accept()     # Establish connection with client.
    thread.start_new_thread(on_new_client,(c,addr))
    print "mail loop"
    #Note it's (addr,) not (addr) because second parameter is a tuple
    #Edit: (c,addr)
    #that's how you pass arguments to functions when creating new threads using thread module.
s.close()

