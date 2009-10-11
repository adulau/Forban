#
# forban UUID

import uuid
import os.path

class manage:

    def __init__ (self, dynpath = "../var/"):

        self.dynpath = dynpath
        self.fidpath = dynpath + "fid" 
        self.create()
    
    def create(self):
 
        if os.path.isdir(self.dynpath) and os.path.isfile(self.fidpath):
            fidfile = open(self.fidpath,'r')
            self.fid = fidfile.read()
            fidfile.close()
        else:
            self.fid = str(uuid.uuid4())
            if not os.path.isdir(self.dynpath):
                os.mkdir(self.dynpath)
            fidfile = open(self.fidpath,'w')
            fidfile.write(str(self.fid))
            fidfile.close()

    def get (self):
        return self.fid

    def regen (self):
        os.unlink(self.fidpath)
        self.create()

def managetest():
        fid = manage()
        print fid.get()
        fid.regen()
        print fid.get()

if __name__ == "__main__":
    
    managetest()
            
