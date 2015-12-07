#!/usr/bin/python

import threading
import socket, string
import time
import sys

def get_file(nama):
    nama=nama+'.jpg'
    print nama
    try:
        myfile = open(nama)
        return myfile.read()
    except:
        return 'wrong syntax bro'

def pisah_string(data):
    data1=data.split(' ',1)
    return data1

def proses(permintaan):
    #print 'yoyo salah kah?'
    data=pisah_string(permintaan)
    data1=pisah_string(data[1])
    if data1[0]=='/':
        return '<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN"><HTML><BODY>Home pageeee</P></BODY></HTML>'
    else:
        return get_file(data1[0][1:])

class MemprosesClient(threading.Thread):
    def __init__(self,client_socket,client_address,nama):
        self.client_socket = client_socket
        self.client_address = client_address
        self.nama = nama
        threading.Thread.__init__(self)
    
    def run(self):
        #print 'im here baby'
        message = ''
        while True:
            data = self.client_socket.recv(32)
            if data:
                message = message + data #collect seluruh data yang diterima
                #print message+'\n\n'
                if (message.endswith("\r\n\r\n")):
                    #print 'hiks hiks'
                    #request=proses(message)
                    self.client_socket.send(proses(message))
                    break
            else:
                print 'error di siniiiiii'
                break
        self.client_socket.close()
        

class Server(threading.Thread):
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('0.0.0.0',9999)
        self.my_socket.bind(self.server_address)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.listen(1)
        nomor=0
        while (True):
            self.client_socket, self.client_address = self.my_socket.accept()
            nomor=nomor+1
            #---- menghandle message cari client (Memproses client)
            my_client = MemprosesClient(self.client_socket, self.client_address, 'PROSES NOMOR '+str(nomor))
            my_client.start()
            #----


serverku = Server()
serverku.start()
