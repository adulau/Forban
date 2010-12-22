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

import sys
import time
import os
import logging
import logging.handlers
import ConfigParser

def guesspath():
    pp = os.path.realpath(sys.argv[0])
    bis = pp.rsplit("/",2)
    return bis[0]

config = ConfigParser.RawConfigParser()
config.read(os.path.join(guesspath(),"cfg","forban.cfg"))

try:
    forbanpath = config.get('global','path')
except ConfigParser.NoOptionError:
    forbanpath = os.path.join(guesspath())

try:
    announceinterval = config.get('global','announceinterval')
except ConfigParser.NoOptionError:
    announceinterval = 10

try:
    forbanshareroot = config.get('forban','share')
except ConfigParser.NoOptionError:
    forbanshareroot = os.path.join(forbanpath,"var","share/")

try:
    forbanlogginglevel = config.get('global','logging')
except ConfigParser.NoOptionError:
    forbanlogginglevel = "INFO"

try:
    forbanloggingsize = config.get('global','loggingmaxsize')
except ConfigParser.NoOptionError:
    forbanloggingsize = 100000


announceinterval = float(announceinterval)
forbanpathlib=os.path.join(forbanpath,"lib")
sys.path.append(forbanpathlib)

import announce
import index

forbanpathlog=os.path.join(forbanpath,"var","log")
if not os.path.exists(forbanpathlog):
    os.mkdir(forbanpathlog)

forbanpathlogfile=forbanpathlog+"/forban_announce.log"
flogger = logging.getLogger('forban_announce')

if forbanlogginglevel == "INFO":
    flogger.setLevel(logging.INFO)
else:
    flogger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(forbanpathlogfile, backupCount=5, maxBytes = forbanloggingsize)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
flogger.addHandler(handler)

if __name__ == "__main__":

    forbanname = config.get('global','name')
    msg = announce.message(name=forbanname)

    forbanindex = index.manage(sharedir=forbanshareroot, forbanglobal=forbanpath)
    flogger.info("forban_announce starting...")
while 1:
    # rebuild forban index
    forbanindex.build()
    msg.gen()
    msg.auth(value=forbanindex.gethmac())
    flogger.debug(msg.get())
    msg.send()
    time.sleep(announceinterval)
