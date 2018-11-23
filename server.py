# The server accepts connection from multiple clients and
# broadcasts data sent by a client to all other clients
# which are online (connection active with server)

import socket
import select
#import string

def broadcast_data (sock, message):



    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            socket.send(message.encode('ascii'))

if __name__ == "__main__":

    # List to keep track of socket descriptors
    CONNECTION_LIST=[]

    # Do basic steps for server like create, bind and listening on the socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 5000))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print("********SERVER STARTED*********")

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

        for sock in read_sockets:

            if sock == server_socket:
                # Handle the case in which there is a new connection recieved
                # through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print ("Client (%s, %s) connected"%addr)
                broadcast_data(sockfd, "Client (%s, %s) connected" % addr)

            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(4096)


                except:
                    broadcast_data(sock, "Client %s is offline"%addr[1])
                    print("Client (%s, %s) is offline"%addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

                if data:
                    # The client sends some valid data, process it
                    data = data.decode('ascii')
                    if data == "q" or data == "Q":
                        broadcast_data(sock, "Client (%s, %s) quits" % addr)
                        print ("Client (%s, %s) quits"%addr)
                        sock.close()
                        CONNECTION_LIST.remove(sock)
                    else:
                        #z=data.decode('ascii')
                        x="Message From Client "
                        y=str(addr[1])+" : "
                        data=x+y+data
                        broadcast_data(sock,data)

    server_socket.close()
