#!/usr/bin/env python
def send_all_data(kvt,host='localhost',port=2003):
    import socket
    data=""
    for key,value,ts in kvt:
        data+="{} {} {}\n".format(key.replace(" ","_"),value,ts)
    print(data)
    sock = socket.socket()
    sock.connect((host, port))
    sock.sendall(data.encode())
    sock.close()

