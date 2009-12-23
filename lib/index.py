import os
import re
import difflib
import re
import sys

import fetch
import loot

class manage:

    def __init__ (self, sharedir="../var/share/",
    location="../var/share/forban/index", forbanglobal = "../"):
        self.location = location
        self.sharedir = sharedir
        self.lootdir = forbanglobal + "/var/loot/";

    def build (self):
        self.index = ""
        for root, dirs, files in os.walk(self.sharedir, topdown=True):
            for name in files:
                self.index = self.index + os.path.join(root.split(self.sharedir)[1],name)+","+str(os.path.getsize(os.path.join(root,name)))+"\n"
        
        f = open (self.location,"w")
        f.write(self.index)
        f.close()

    def cache (self, uuid):
        cachepath = self.lootdir + uuid + "/cache"
        if not os.path.exists(cachepath):
            os.mkdir(cachepath)
        lloot = loot.loot()
        for url in lloot.getindexurl(uuid):
            fetch.urlget(url, cachepath+"/forban/index")

    def howfar (self, uuid):
        cachepath = self.lootdir + uuid + "/cache/forban/index"
        # how can I compare my cache to the other, if the other
        # cache is missing...
        if not os.path.exists(cachepath):
            return False
        f1 = open(self.location,"r")
        f1v = f1.read()
        f1.close()
        f2 = open(cachepath,"r")
        f2v = f2.read()
        f2.close()
        mydiff = '\n'.join(list(difflib.unified_diff(f1v.splitlines(),f2v.splitlines(), lineterm="")))
        lmodified = []
        for l in mydiff.splitlines():
            if re.search("(^\+)",l) and not re.search("^\+\+",l) and not re.search("forban",l):
               missingfile = l.rsplit(",",1)[0]
               missingfile = re.sub("^(\+)","",missingfile)
               lmodified.append(missingfile)
        return lmodified

def test ():
    testindex = manage()
    testindex.build()
    testindex.cache("cb001bf2-1497-443c-9675-74de7027ecf9")
    print testindex.howfar("e2f05993-eba1-4b94-8e56-d2157d1ce552")

if __name__ == "__main__":

    test()
