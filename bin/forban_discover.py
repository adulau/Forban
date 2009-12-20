
import sys
import time

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read("../cfg/forban.cfg")

forbanpath = config.get('global','path')


sys.path.append(forbanpath+"lib/")

import discover


if __name__ == "__main__":

    while 1:
        HOST, PORT = ("::",12555)
        server = discover.UDPServer((HOST, PORT), discover.MyUDPHandler)
        server.serve_forever()

