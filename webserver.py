#!/usr/bin/python

import socket, select, string

def pisah_string(data):
    data1=data.split(' ',1)
    return data1

def proses_data(sock, data):
    data1=pisah_string(data)
    #print data1
    if data1[0]=='GET':
        gett(sock, data1[1])
    else:
        print "SERVER: ERR 9996 - Wrong recieved data"
        sock.send(9996)

def gett(sock, data):
    sock.send("HTTP/1.1 200 OK\n\nSo sad it must be closed")
    print "Sending data get"
    sock.close()
    CONNECTION_LIST.remove(sock)
    return

if __name__ == "__main__":
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    NAME_LIST = []
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 10000))
    server_socket.listen(10)
 
    # Add server socket to the list
    CONNECTION_LIST.append(server_socket)

    tmp=''
 
    while 1:
        # Get socket list
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "New client %s, %s" %addr
                 
                #broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
             
            #Recieve message
            else:
                try:    
                    data = sock.recv(4069)
                    if data:
                        tmp=tmp+data
                        print tmp
                        proses_data(sock, data)
                 
                except:
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    #print tmp+" \n\n"

     
    server_socket.close()