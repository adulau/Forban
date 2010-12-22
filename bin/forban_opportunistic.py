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

import glob
import os.path
import sys
import string
import time
import ConfigParser
import re
import logging
import logging.handlers

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
    forbanshareroot = config.get('forban','share')
except ConfigParser.NoOptionError:
    forbanshareroot = os.path.join(forbanpath,"var","share/")
except ConfigParser.NoOptionError:
    forbanpath = os.path.join(guesspath())
    forbanshareroot = os.path.join(forbanpath,"var","share/")

forbanpathlib = os.path.join(forbanpath,"lib")
sys.path.append(forbanpathlib)
import index
import loot
import fetch
import base64e

if not config.get("global","mode") == "opportunistic":
    print "not configured in opportunistic mode"
    exit(1)


try:
    announceinterval = config.get('global','announceinterval')
except ConfigParser.NoOptionError:
    announceinterval = 10

announceinterval = float(announceinterval)

try:
    forbanlogginglevel = config.get('global','logging')
except ConfigParser.NoOptionError:
    forbanlogginglevel = "INFO"

try:
    forbanloggingsize = config.get('global','loggingmaxsize')
except ConfigParser.NoOptionError:
    forbanloggingsize = 100000

forbanpathlog=os.path.join(forbanpath,"var","log")
if not os.path.exists(forbanpathlog):
    os.mkdir(forbanpathlog)

forbanpathlogfile=forbanpathlog+"/forban_opportunistic.log"
flogger = logging.getLogger('forban_opportunistic')

if forbanlogginglevel == "INFO":
    flogger.setLevel(logging.INFO)
else:
    flogger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(forbanpathlogfile, backupCount=5, maxBytes = forbanloggingsize)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
flogger.addHandler(handler)

try:
    ofilter = config.get('opportunistic','filter')
except ConfigParser.NoOptionError:
    ofilter = ""

try:
    efilter = config.get('opportunistic','efilter')
except ConfigParser.NoOptionError:
    efilter = None

refilter = re.compile(ofilter, re.I)
if efilter is not None:
    exfilter = re.compile(efilter, re.I)
else:
    exfilter = re.compile("", re.I)

try:
    maxsize = config.get('opportunistic','maxsize')
except ConfigParser.NoOptionError:
    maxsize = 0

discoveredloot = loot.loot()
allindex = index.manage(sharedir=forbanshareroot, forbanglobal=forbanpath)
allindex.build()

flogger.info("forban_opportunistic starting...")
flogger.info("applied including regexp filter: %s" % ofilter)
flogger.info("applied excluding regexp filter: %s" % efilter)
while(1):

    for uuid in discoveredloot.listall():

        # check if my loot is not exceeding the maxsize
        mysize = allindex.totalfilesize(discoveredloot.whoami())
        if float(maxsize) != 0:
            if mysize is False:
                continue
            if float(mysize[:-2])>float(maxsize):
                flogger.info("maxsize exceeded (current:%s - max:%sGB)" % (mysize, maxsize))
                continue
        # fetch the index of all discovered and recently announced loots
        # allowing to compare local loot to announced loot
        if discoveredloot.exist(uuid) and discoveredloot.lastannounced(uuid):
            allindex.cache(uuid)

        if not discoveredloot.lastannounced(uuid):
            flogger.info("%s (%s) not seen recently, skipped" % (discoveredloot.getname(uuid),(uuid)))
            continue

        missingfiles = allindex.howfar(uuid)
        # avoid comparing with ourself
        if not missingfiles or (discoveredloot.whoami() == uuid):
            flogger.info("missing no files with %s (%s)" % (discoveredloot.getname(uuid),uuid))
        else:
            for missedfile in missingfiles:
                if re.search(refilter, missedfile) and not (re.search(exfilter, missedfile) and efilter is not None):
                    sourcev4 = discoveredloot.getipv4(uuid)
                    url =  """http://%s:12555/s/?g=%s&f=b64e""" % (sourcev4, base64e.encode(missedfile))
                    localfile = forbanshareroot + "/" + missedfile
                    localsize = allindex.getfilesize(filename=missedfile)
                    remotesize = allindex.getfilesize(filename=missedfile,uuid=uuid)
                    if localsize < remotesize:
                        flogger.info("local file smaller - from %s fetching %s to be saved in %s" % (uuid,url,localfile))
                        fetch.urlget(url,localfile)
                    elif localsize is False:
                        flogger.info("local file not existing - from %s fetching %s to be saved in %s" % (uuid,url,localfile))
                        fetch.urlget(url,localfile)
                    elif remotesize is False:
                        flogger.info("remote file index issue for %s on loot %s" % (missedfile, uuid))
                    else:
                        flogger.info("local file larger or corrupt %s - don't fetch it" % (localfile))
                    allindex.build()

    time.sleep(announceinterval*(announceinterval/(announceinterval-2)))

