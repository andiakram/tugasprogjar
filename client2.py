#!/usr/bin/python

import socket, select, string, sys, time

username=[]

#print you tiap kali
def prompt():
    sys.stdout.write("<you> ")
    sys.stdout.flush()

def pisah_string(data):
    data1=data.split(' ',1)
    return data1

def print_err(code):
    if code ==5001:
        print "CLIENT: ERR 5001 - No message sent, enter your message"
    elif code==5002:
        print "CLIENT: ERR 5002 - No message sent, enter recipient username and your message"
    elif code==5003:
        print "CLIENT: ERR 5003 - No message sent, invalid recipient"
    elif code ==9999:
        print "CLIENT: ERR 9999 - Wrong syntax"
    elif code==9998:
        print "SERVER: ERR 9998 - Wrong syntax"
    elif code==9997:
        print "CLIENT: ERR 9997 - Wrong recieved data"
    else:
        if code ==4001:
            print "SERVER: ERR 4001 - Can\'t login, username already exist"
        elif code ==4002:
            print "SERVER: ERR 4002 - Can\'t login, you are already login"
        elif code ==4101:
            print "CLIENT: ERR 4101 - Can\'t login, username and password is same, please change it"

        print "\nSystem will be closed"
        sys.exit()

def login(sock):
    print "Enter your username : "
    usname=sys.stdin.readline()
    sys.stdin.flush()
    usname1=pisah_string(usname)
    print "Enter your password : "
    passw=sys.stdin.readline()
    passw1=pisah_string(passw)
    #print usname1+passw1
    if usname1==passw1: print_err(4101)
    else: sock.send("login "+usname1[0]+" "+passw1[0])

def terima_data(sock):
    #menerima data
    data=sock.recv(4096)
    #jika tidak ada data yang diterima
    if not data:
        print "\rDisconnected from chat server"
        sys.exit()
    else:
        data1=pisah_string(data)
        if data1[0]=="2000":
            #menyimpan username dan status login
            username=data1[1]
            sys.stdout.write("{}\rOk, your name is "+data1[1]+"\n")
            sys.stdout.flush()
        elif data1[0]=="2001":
            sys.stdout.write("{}\r"+data1[1])
            sys.stdout.flush()
        elif data1[0]=="2002":
            sys.stdout.write("{}\r"+data1[1])
            sys.stdout.flush()
            print "Ok, system will be closed. Goodbye!"
            sys.exit()
        elif data1[0]=="4001":
            print_err(4001)
        elif data1[0]=="4002":
            print_err(4002)
        elif data1[0]=="5003":
            print_err(5003)
        else:
            print_err(9997)

def kirim_data(sock):
    msg=sys.stdin.readline()
    msg1=pisah_string(msg)
    msg2=string.split(msg)
    #print ukuran
    ukuran=len(msg2)
    #print msg1[0][:-1]
    if msg1[0][:-1]=="sendall" and ukuran<2:
        print_err(5001)
    elif msg1[0]=="sendall":
        sock.send(msg)
    elif msg1[0][:-1]=="sendto" and ukuran<2:
        print_err(5002)
    elif msg1[0]=="sendto" and ukuran<3:
        print_err(5001)
    elif msg1[0]=="sendto":
        sock.send(msg)
    elif msg1[0][:-1]=="list" and ukuran<2:
        sock.send(msg)
    elif msg1[0][:-1]=="logout" and ukuran<2:
        sock.send(msg)
    else:
        print_err(9999)

#main function
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #coba connect ke server
    try :
        s.connect(("0.0.0.0", 5000))
    except :
        print "Unable to connect"
        sys.exit()
     
    print "Connected to remote host."
 
    login(s)
 
    #prompt()
 
    while 1:
        socket_list=[sys.stdin, s]
 
        #membaca socket yang ada
        read_sockets, write_sockets, error_sockets=select.select(socket_list , [], [])
 
        for sock in read_sockets:
            if sock==s:
                terima_data(sock)
                prompt()
 
            else:
                kirim_data(s)
                prompt()