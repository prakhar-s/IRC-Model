# The client program connects to server and sends data to other connected
# clients through the server
import socket

import sys

from _thread import *
import threading


def recv_data():
    #"Receive data from other clients connected to server"
    while 1:
        try:
            recv_data = client_socket.recv(4096)
        except:
            #Handle the case when server process terminates
            print ("Server closed connection, thread exiting.")
            interrupt_main()
            break
        if not recv_data:
                # Recv with no data, server closed connection
                print ("Server closed connection, thread exiting.")
                #interrupt_main()
                break
        else:
                print ("\nReceived data: ", recv_data.decode('ascii'))

def send_data():
    #"Send data from other clients connected to server"
    while 1:
        send_data = str(input("Enter your message to send (q or Q to quit):"))
        if send_data == "q" or send_data == "Q":
            client_socket.send(send_data.encode('ascii'))
            interrupt_main()
            break
        else:
            client_socket.send(send_data.encode('ascii'))

if __name__ == "__main__":

    print ("*******CLIENT STARTED********")
    print ("Connecting to server at 127.0.0.1:5000")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5000))

    print ("Connected to server at 127.0.0.1:5000")

    start_new_thread(recv_data,())
    start_new_thread(send_data,())

    try:
        while 1:
            continue
    except:
        print ("Client program quits....")
        client_socket.close()
