# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2011 Alexandre Dulaunoy - http://www.foo.be/
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
    lpath = os.path.split(pp)
    bis = os.path.split(lpath[0])
    return bis[0]

config = ConfigParser.RawConfigParser()
config.read(os.path.join(guesspath(),"cfg","forban.cfg"))


try:
    forbanpath = config.get('global','path')
except ConfigParser.Error:
    forbanpath = os.path.join(guesspath())

try:
    forbanshareroot = config.get('forban','share')
except ConfigParser.Error:
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

try:
    forbanmode = config.get('global','mode')
except ConfigParser.Error:
    forbanmode = "opportunistic"


try:
    forbanlogginglevel = config.get('global','logging')
except ConfigParser.Error:
    forbanlogginglevel = "INFO"

try:
    forbanloggingsize = config.get('global','loggingmaxsize')
except ConfigParser.Error:
    forbanloggingsize = 100000

forbanpathlog=os.path.join(forbanpath,"var","log")
if not os.path.exists(forbanpathlog):
    os.mkdir(forbanpathlog)

forbanpathlogfile=os.path.join(forbanpathlog,"forban_opportunistic_fs.log")

flogger = logging.getLogger('forban_opportunistic_fs')

if forbanlogginglevel == "INFO":
    flogger.setLevel(logging.INFO)
else:
    flogger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(forbanpathlogfile, backupCount=5, maxBytes = forbanloggingsize)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
flogger.addHandler(handler)

try:
    forbanopportunisticfsdir = config.get('opportunistic_fs','directory')
except ConfigParser.Error:
    flogger.info("not started / no configuration present")
    exit(1)

if forbanopportunisticfsdir == "":
    flogger.info("not started - directory not set")
    exit(1)

flogger.info("starting using input/output directory %s",forbanopportunisticfsdir)
flogger.info("using mode %s",forbanmode)
