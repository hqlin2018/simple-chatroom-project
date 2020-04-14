import socket
import threading

outstring = ''
instring = ''
nike = ''

def client_send(sock):
    global outstring
    while True:
        outstring = input()
        outstring = nike + ':' +outstring
        sock.send(outstring.encode())

def client_accept(sock):
    global instring
    while True:
        try:
            instring = sock.recv(1024).decode()
            if not instring:
                break
            if outstring != instring:
                print (instring)
        except:
            break
        
nike = input('input your nikename:')
ip = input('input the server ip address:')
port = 8080

sock = socket.socket()
sock.connect((ip, port))

sock.send(nike.encode())

th_send = threading.Thread(target=client_send , args=(sock, ))
th_send.start()

th_accept = threading.Thread(target=client_accept, args=(sock,))
th_accept.start()
