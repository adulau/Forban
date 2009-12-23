import os
import re

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
        
def test ():
    testindex = manage()
    testindex.build()
    testindex.cache("cb001bf2-1497-443c-9675-74de7027ecf9")

if __name__ == "__main__":

    test()
