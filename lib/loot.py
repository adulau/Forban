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

import os.path
import re
import datetime
import time
import sys

# forban internal junk
sys.path.append('.')
import fid
import tmpname
import tools

class loot:

    def __init__ (self, dynpath = "../var/"):

        self.dynpath = dynpath
        self.lootpath = os.path.join(dynpath,"loot")
        if not os.path.isdir(self.lootpath):
            os.mkdir(self.lootpath)

    def listall (self):
        lloot =  []
        for root, dirs, files in os.walk(self.lootpath, topdown=True):
            for name in dirs:
                if "cache" not in os.path.join(root,name):
                    lloot.append(name)
        return lloot

    def getname (self, uuid):

        pathname = os.path.join(self.lootpath,uuid,"name")

        if os.path.exists(pathname):
            f = open (pathname)
            rname = f.read()
            f.close();
            return rname
        else:
            return None

    def getipv4 (self, uuid):

        pathsourcev4 = os.path.join(self.lootpath,uuid,"sourcev4")

        if os.path.exists(pathsourcev4):
            f = open (pathsourcev4)
            rname = f.read()
            f.close()
            return rname
        else:
            return None

    def getlastseen (self, uuid):

        pathlastseen = os.path.join(self.lootpath,uuid,"last")
        defaultlastseen = 100
        if self.exist(uuid):

            if os.path.exists(pathlastseen):
                try:
                    f = open (pathlastseen)
                    rlastseen = f.read()
                    f.close()
                except:
                    rlastseen = defaultlastseen

                return rlastseen
            else:
                return defaultlastseen
        else:

            return defaultlastseen

    def lastannounced (self, uuid, timeago=300):

        lastseen = float(self.getlastseen(uuid))
        t = datetime.datetime.now()
        now = time.mktime(t.timetuple())
        gap = now-lastseen
        if gap < timeago:
            return gap
        else:
            return False

    def whoami (self):

        lfid = fid.manage(dynpath=self.dynpath)
        return lfid.get()

    def getipv6 (self, uuid):

        pathsourcev6 = os.path.join(self.lootpath,uuid,"sourcev6")

        if os.path.exists(pathsourcev6):
            f = open (pathsourcev6)
            rname = f.read()
            f.close()
            return rname
        else:
            return None

    def exist (self, uuid):

        aloot = os.path.join(self.lootpath,uuid)
        if os.path.isdir(aloot):
            return True
        else:
            return False

    def getindexurl (self, uuid, v4only=False):
        iurl = []

        if self.exist(uuid):
            ipv4 = self.getipv4(uuid)
            if ipv4 is not None:
                iurl.append("http://"+ipv4+":12555/s/?g=forban/index")
            ipv6 = self.getipv6(uuid)
            if not v4only:
                if ipv6 is not None:
                    iurl.append("http://["+ipv6+"]:12555/s/?g=forban/index")
            return iurl
        else:
            return False

    def add (self, dmessage, sip):

        mess = dmessage.split(";")
        self.hmac = None
        for i in range (1, len(mess)-1, 2):
            if mess[i] == "name":
                #name is REQUIRED
                self.lname = mess[i+1]
            elif mess[i] == "uuid":
                #uuid is REQUIRED
                self.luuid = mess[i+1]
            elif mess[i] == "hmac":
                #hmac is RECOMMENDED
                self.hmac = mess[i+1]
        self.lsource = sip

        if not self.exist(self.luuid):
            os.mkdir(os.path.join(self.lootpath,self.luuid))

        if self.hmac is not None:
            self.sethmac(lhmac=self.hmac)

        self.setfirstseen()
        self.setlastseen()

        if re.search(":",self.lsource):
            if re.match("^::ffff:",self.lsource):
                self.lsourcev4 = re.sub("^::ffff:","",self.lsource)
                self.lsourcev6 = None
            else:
                # IPv6 link-local regularly uses the interface source
                # to deduce where to send the request when multiple
                # interface with IPv6 link-local are enable.
                #self.lsourcev6 = self.lsource.split("%")[0]
                # we now keep the source interface too.
                # but in such case web url are only accessible to
                # the local machine or machine matching same interface name.
                self.lsourcev6 = self.lsource
                self.lsourcev4 = None
        else:
            self.lsourcev4 = self.lsource
            self.lsourcev6 = None

        self.setname(self.lname)
        self.setsource(self.lsourcev4, self.lsourcev6)

    def setname (self, lname):

        localfile =  os.path.join(self.lootpath,self.luuid,"name")
        tlocalfile = tmpname.get(localfile)

        f = open(tlocalfile[1], "w")
        f.write(lname)
        f.close()

        tools.rename(tlocalfile[1], tlocalfile[0])

        # self is added for the same forban doing the announce
        # and the discovery

        myid = fid.manage(dynpath=self.dynpath)
        if myid.get() == self.luuid:
            localfile = os.path.join(self.lootpath,self.luuid,"self")
            tlocalfile = tmpname.get(localfile)
            f = open (tlocalfile[1], "w")
            f.write("")
            f.close()
            tools.rename(tlocalfile[1], tlocalfile[0])

    def sethmac (self, lhmac = None):

        localfile = os.path.join(self.lootpath,self.luuid,"hmac")
        tlocalfile = tmpname.get(localfile)

        f = open(tlocalfile[1], "w")
        f.write(lhmac)
        f.close()

        tools.rename(tlocalfile[1], tlocalfile[0])


    def gethmac (self, uuid):

        pathhmac = os.path.join(self.lootpath,uuid,"hmac")

        if self.exist(uuid):
            if os.path.exists(pathhmac):
                f = open (pathhmac)
                rhmac = f.read()
                f.close()
                return rhmac
            else:
                return None
        else:

            return None

    def setsource (self, sourcev4 = None , sourcev6 = None):

        if sourcev4 is not None:
            f = open(os.path.join(self.lootpath,self.luuid,"sourcev4"), "w")
            f.write(sourcev4)
            f.close()
        if sourcev6 is not None:
            f = open(os.path.join(self.lootpath,self.luuid,"sourcev6"), "w")
            f.write(sourcev6)
            f.close()

    def setfirstseen (self):

        firstseenpath = os.path.join(self.lootpath,self.luuid,"first")
        if not os.path.exists(firstseenpath):
            f = open(firstseenpath, "w")
            t = datetime.datetime.now()
            f.write(str(time.mktime(t.timetuple())))
            f.close()

    def setlastseen (self):

        localfile =  os.path.join(self.lootpath,self.luuid,"last")
        tlocalfile = tmpname.get(localfile)
        f = open(tlocalfile[1], "w")
        t = datetime.datetime.now()
        f.write(str(time.mktime(t.timetuple())))
        f.close()
        if os.path.exists(tlocalfile[1]):
            tools.rename(tlocalfile[1], tlocalfile[0])

def loottest():

        myloot = loot()
        if not myloot.exist("1234"):
            print "not existing -> ok"
        #myloot.add("forban;name;notset;uuid;cb001bf2-1497-443c-9675-74de7027ecf9;hmac;59753cbda00f8c605aff6c4ceacd3f12caedddea","127.0.0.1")
        print myloot.getindexurl("cb001bf2-1497-443c-9675-74de7027ecf9")
        print myloot.getlastseen("cb001bf2-1497-443c-9675-74de7027ecf9")
        print myloot.lastannounced("cb001bf2-1497-443c-9675-74de7027ecf9")
        print myloot.listall()
        print myloot.gethmac("cb001bf2-1497-443c-9675-74de7027ecf9")

if __name__ == "__main__":

    loottest()
