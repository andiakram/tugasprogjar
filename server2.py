#!/usr/bin/python

import socket, select, string

def pisah_string(data):
    data1=data.split(' ',1)
    return data1

def proses_data(sock, data):
    data1=pisah_string(data)
    #print data1
    if data1[0]=='login':
        log_in(sock, data1[1])
    elif data1[0]=='sendall':
        send_all(sock, data1[1])
    elif data1[0]=='sendto':
        send_to(sock, data1[1])
    elif data1[0][:-1]=='list':
        minta_list(sock)
    elif data1[0][:-1]=='logout':
        log_out(sock)
    else:
        print "SERVER: ERR 9996 - Wrong recieved data"
        sock.send(9996)


def cek_nama(sock):
    namaa=[]
    for x in range (len(NAME_LIST)):
        if NAME_LIST[x]==sock:
            namaa=NAME_LIST[x+1]
            namaa=pisah_string(namaa)

    return namaa[0]

def cek_socket(data):
    sockeet=[]
    for x in range (len(NAME_LIST)):
        tmp=str(NAME_LIST[x])
        spasi=tmp.count(' ')
        if spasi>0:
            namaa=pisah_string(tmp)
            if namaa[0][:-1]==data:
                sockeet=NAME_LIST[x-1]
                continue

    return sockeet

def log_in(sock, data):
    ceknama=0
    ceksock=0

    pecah=pisah_string(data)
    name=pecah[0]
    password=pecah[1]

    for x in NAME_LIST:
        xx=pisah_string(str(x))
        if xx[0]==sock: ceksock=1
        if xx[0]==name: ceknama=1

    if ceknama==1:
        print "SERVER: ERR 4001 - Can\'t login, username already exist"
        sock.send("4001")
        sock.close()
    elif ceksock==1:
        print "SERVER: ERR 4002 - Can\'t login, you are already login"
        sock.send("4002")
        sock.close()
    else:
        print name[:-1]+" have login with password "+password[:-1]
        NAME_LIST.append(sock)
        NAME_LIST.append(name+" "+password)
        sock.send("2000 "+name[:-1])

def send_all(sock, data):
    sender=cek_nama(sock)
    print "Sending message from "+sender[:-1]+" to all"
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            socket.send("2001 <sendall from "+sender[:-1]+"> "+data)

def send_to(sock, data):
    sender=cek_nama(sock)
    pecah=pisah_string(data)
    recipient_socket=[]
    recipient_socket=cek_socket(pecah[0])
    if not recipient_socket:
        sock.send("5003")
        return 0
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket == recipient_socket :
            socket.send("2001 <pm from "+sender[:-1]+"> "+pecah[1])
            print "Sending message from "+sender[:-1]+" to "+pecah[0]
            return

def minta_list(sock):
    sender=cek_nama(sock)
    print "Sending list to "+sender[:-1]
    for x in range (len(NAME_LIST)):
        if x%2==1 and sock!=NAME_LIST[x-1]:
            namaa=pisah_string(str(NAME_LIST[x]))
            sock.send("2001 List: "+str(namaa[0]))

def log_out(sock):
    for x in range (len(NAME_LIST)):
        if NAME_LIST[x]==sock:
            namaa=pisah_string(str(NAME_LIST[x+1]))
            print namaa[0][:-1]+" have logout"
            sock.send("2002 Ok goodbye "+namaa[0])
            NAME_LIST.remove[x]
            NAME_LIST.remove[x+1]
            NAME_LIST.remove[x+2]
            sock.close()
            CONNECTION_LIST.remove(sock)
            return

if __name__ == "__main__":
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    NAME_LIST = []
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 5000))
    server_socket.listen(10)
 
    # Add server socket to the list
    CONNECTION_LIST.append(server_socket)
 
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
                        proses_data(sock, data)
                 
                except:
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()