
import os.path
import re
import datetime
import time
import sys

# forban internal junk
sys.path.append('.')
import fid

class loot:

    def __init__ (self, dynpath = "../var/"):

        self.dynpath = dynpath
        self.lootpath = dynpath + "loot/" 
        if not os.path.isdir(self.lootpath):
            os.mkdir(self.lootpath)

    def getname (self, uuid):

        pathname = self.lootpath+"/"+uuid+"/name"

        if os.path.exists(pathname):
            f = open (pathname);
            rname = f.read();
            f.close();
            return rname
        else:
            return None

    def getipv4 (self, uuid):

        pathsourcev4 = self.lootpath+"/"+uuid+"/sourcev4"

        if os.path.exists(pathsourcev4):
            f = open (pathsourcev4);
            rname = f.read();
            f.close();
            return rname
        else:
            return None

    def whoami (self):
        
        lfid = fid.manage()
        return lfid.get()

    def getipv6 (self, uuid):

        pathsourcev6 = self.lootpath+"/"+uuid+"/sourcev6"

        if os.path.exists(pathsourcev6):
            f = open (pathsourcev6);
            rname = f.read();
            f.close();
            return rname
        else:
            return None
 
    def _exist (self, uuid):

        aloot = self.lootpath+uuid+"/"
        if os.path.isdir(aloot):
            return True
        else:
            return False

    def add (self, dmessage, sip):
        
        mess = dmessage.split(";")
        self.lname = mess[2]
        self.luuid = mess[4]
        self.lsource = sip

        if not self._exist(self.luuid):
            os.mkdir(self.lootpath+self.luuid)

        self.setfirstseen()
        self.setlastseen()

        if re.search(":",self.lsource):
            if re.match("^::ffff:",self.lsource):
                self.lsourcev4 = re.sub("^::ffff:","",self.lsource)
                self.lsourcev6 = None
            else:
                self.lsourcev6 = self.lsource.split("%")[0]
                self.lsourcev4 = None
        else:
            self.lsourcev4 = self.lsource
            self.lsourcev6 = None

        self.setname(self.lname)
        self.setsource(self.lsourcev4, self.lsourcev6)

    def setname (self, lname):
        
        f = open(self.lootpath+self.luuid+"/"+"name", "w")
        f.write(lname)
        f.close()

        # self is added for the same forban doing the announce
        # and the discovery

        myid = fid.manage()
        if myid.get() == self.luuid:
            f = open (self.lootpath+self.luuid+"/"+"self", "w")
            f.write("")
            f.close()

    def setsource (self, sourcev4 = None , sourcev6 = None):
        
        if sourcev4 is not None:
            f = open(self.lootpath+self.luuid+"/"+"sourcev4", "w")
            f.write(sourcev4)
            f.close()
        if sourcev6 is not None:
            f = open(self.lootpath+self.luuid+"/"+"sourcev6", "w")
            f.write(sourcev6)
            f.close()

    def setfirstseen (self):
        
        firstseenpath = self.lootpath+self.luuid+"/"+"first"
        if not os.path.exists(firstseenpath):
            f = open(firstseenpath, "w")
            t = datetime.datetime.now()
            f.write(str(time.mktime(t.timetuple())))
            f.close()

    def setlastseen (self):
        
        lastseenpath = self.lootpath+self.luuid+"/"+"last"
        f = open(lastseenpath, "w")
        t = datetime.datetime.now()
        f.write(str(time.mktime(t.timetuple())))
        f.close()


def loottest():
        
        myloot = loot()
        if not myloot._exist("1234"):
            print "not existing -> ok"
        myloot.add("forban;name;notset;uuid;cb001bf2-1497-443c-9675-74de7027ecf9;hmac;59753cbda00f8c605aff6c4ceacd3f12caedddea","127.0.0.1");

if __name__ == "__main__":
    
    loottest()
