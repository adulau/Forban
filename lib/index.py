import os
import re

class manage:

    def __init__ (self, sharedir="../var/share/", location="../var/share/forban/index"):
        self.location = location
        self.sharedir = sharedir

    def build (self):
        self.index = ""
        for root, dirs, files in os.walk(self.sharedir, topdown=True):
            for name in files:
                self.index = self.index + os.path.join(root.split(self.sharedir)[1],name)+","+str(os.path.getsize(os.path.join(root,name)))+"\n"
        
        f = open (self.location,"w")
        f.write(self.index)
        f.close()

def test ():
    testindex = manage()
    testindex.build()

if __name__ == "__main__":

    test()
