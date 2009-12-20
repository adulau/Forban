
import sys
import time

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read("../cfg/forban.cfg")

forbanpath = config.get('global','path')


sys.path.append(forbanpath+"lib/")

import announce


if __name__ == "__main__":

    forbanname = config.get('global','name')
    msg = announce.message(name=forbanname)

while 1:
    msg.gen()
    msg.send()
    time.sleep(60)
