
import sys
import time

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read("../cfg/forban.cfg")

forbanpath = config.get('global','path')


sys.path.append(forbanpath+"lib/")

import announce
import index

if __name__ == "__main__":

    forbanname = config.get('global','name')
    msg = announce.message(name=forbanname)

    forbanindex = index.manage()

while 1:
    # rebuild forban index
    forbanindex.build()
    msg.gen()
    msg.send()
    time.sleep(60)
