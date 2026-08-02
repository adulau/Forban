# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2010 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socketserver
import socket
import sys
import os
# forban internal junk
sys.path.append('.')
import loot

def guesspath():
    pp = os.path.realpath(sys.argv[0])
    lpath = os.path.split(pp)
    bis = os.path.split(lpath[0])
    return bis[0]

forbanpath = os.path.join(guesspath())

class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        if isinstance(data, bytes):
            data = data.decode("utf-8", errors="ignore")
        socket = self.request[1]
        if data[:6] == "forban":
            myloot = loot.loot(dynpath=os.path.join(forbanpath,"var"))
            myloot.add(data, self.client_address[0])
        else:
            print("debug : not a forban message")

class UDPServer(socketserver.UDPServer):
    
    def setIPv6 (self, ipv6 = 1 ):
        if  ipv6 == 0 :
            self.disable_ipv6 = 1
        else:
            self.disable_ipv6 = 0

    def useIPv6 (self ):
        return getattr(self, "disable_ipv6", 0) != 1


    if socket.has_ipv6 :
        try:
            socktest = socket.socket(socket.AF_INET6)
            socktest.close()
            address_family = socket.AF_INET6
        except:
            address_family = socket.AF_INET

    def server_bind(self):

        if self.useIPv6() and self.address_family == socket.AF_INET6:

             self.v6success = True
             try:
                 socktest = socket.socket(socket.AF_INET6)
                 socktest.close()
             except:
                 self.v6success = False

             if socket.has_ipv6 and self.v6success:
                 address_family = socket.AF_INET6

             #allowing to work in dual-stack when IPv6 is used
             if socket.has_ipv6 and self.v6success:
                 self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
          
        self.socket.bind(self.server_address)
        # Keep the effective address (notably an OS-selected port) in sync
        # with socketserver's normal server_bind implementation.
        self.server_address = self.socket.getsockname()

if __name__ == "__main__":

   HOST, PORT = ("::",12555)
   server = UDPServer((HOST, PORT), MyUDPHandler)
   server.serve_forever()
