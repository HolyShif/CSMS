import socket

SERVER = "www.adafruit.io"

def check_connection(hostname):
    try:
        #do DNS lookup for hostname
        host = socket.gethostbyname(hostname)
        skt = socket.create_connection((host,80),2)
        print "successful connection to " + SERVER + "\n"
        return True
    except:
        pass
    print "failed connection to " + SERVER + "\n"
    return False

inet_connected = check_connection(SERVER)
print inet_connected
