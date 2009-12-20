import SocketServer
import socket
import sys
# forban internal junk
sys.path.append('.')
import loot

class MyUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        if data[:6] == "forban":
            myloot = loot.loot()
            myloot.add(data, self.client_address[0])
        else:
            print "debug : not a forban message"

class UDPServer(SocketServer.UDPServer):
    if socket.has_ipv6:
        address_family = socket.AF_INET6
    def server_bind(self):
        #allowing to work in dual-stack when IPv6 is used
        if socket.has_ipv6:
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        self.socket.bind(self.server_address)

if __name__ == "__main__":
   HOST, PORT = ("::",12555)
   server = UDPServer((HOST, PORT), MyUDPHandler)
   server.serve_forever()

