#
# forban UUID

import uuid
import os.path

class manage:

    def __init__ (self, dynpath = "../var/"):

        self.dynpath = dynpath
        self.fidpath = dynpath + "fid" 
        
        if os.path.isdir(self.dynpath) and os.path.isfile(self.fidpath):
            print "exit"
        else:
            self.fid = uuid.uuid4()
            print "not existing"

    def get (self):
        return self.fid


def managetest():
        fid = manage();
        print fid.get();

if __name__ == "__main__":
    
    managetest()
            
