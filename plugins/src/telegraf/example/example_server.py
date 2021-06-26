import socket

sock = socket.socket()
print("Socket created ...")

port = 4030
sock.bind(('127.0.0.1', port))
sock.listen(5)

print('socket is listening')

while True:
    c, addr = sock.accept()
    print('got connection from ', addr)

    jsonReceived = c.recv(1024)
    print("Json received -->", jsonReceived)
        
    jsonToSend = b'{"STATUS": "foobar","id": 1}\n'
    c.sendall(jsonToSend)
    print("Json sended -->", jsonToSend)

    c.close()
