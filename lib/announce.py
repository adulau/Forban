import socket
import string
import time
import datetime
import hashlib, hmac
import re
import sys

# forban internal junk
sys.path.append('.')
import fid

class message:

    def __init__(self,name="notset", uuid=None, port="12555", timestamp=None,
    auth=None, destination=["ff02::1","255.255.255.255", ]):
            
            self.name       = name
            self.uuid       = uuid
            self.port       = port
            self.count      = 0
            self.destination = destination

    def gen (self):
            self.payload    = "forban;name;" + self.name + ";"
            myid = fid.manage()
            self.payload    = self.payload + "uuid;" + myid.get()

# the HMAC value is currently useless as the URL is built on
# on the source address of the packet. TBU

    def auth(self,key=None):

        if key is None:
            self.payload = self.payload
        else:
            auth = hmac.new(key, self.payload, hashlib.sha1)
            self.payload = self.payload + ";hmac;" + auth.hexdigest()

    def get (self):
            return self.payload

    def send(self):
        for destination in self.destination:
           
            if socket.has_ipv6 and re.search(":", destination):
                sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                # Required on some version of MacOS X while sending IPv6 UDP
                # datagram
                sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
           
            try:
                sock.sendto(self.payload, (destination, int(self.port)))
            except socket.error, msg:
                continue
        sock.close()



def managetest():
   
    msg = message()
    msg.gen()
    msg.auth()
    print msg.get()
    msg.send()
    msg.auth("forbankey")
    print msg.get()

if __name__ == "__main__":
                                       
    managetest()

