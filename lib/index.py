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

import os
import re
import difflib
import re
import sys
try:
    from hashlib import sha1
except ImportError:
    from sha import sha as sha1

import hmac

import fetch
import loot
import tmpname
import tools

class manage:

    def __init__ (self, sharedir="../var/share/",
    location="../var/share/forban/index", forbanglobal = "../"):
        self.location = sharedir+"/forban/index"
        self.sharedir = sharedir
        self.lootdir = os.path.join(forbanglobal,"var","loot/")

    def build (self):
        self.index = ""
        for root, dirs, files in os.walk(self.sharedir, topdown=True):
            for name in files:
                try:
                    self.index = self.index + os.path.join(root.split(self.sharedir)[1],name)+","+str(os.path.getsize(os.path.join(root,name)))+"\n"
                except:
                    pass

        pid = os.getpid()
        workingloc = self.location+"."+str(pid)
        f = open (workingloc,"w")
        f.write(self.index)
        f.close()
        hmacval = self.calchmac(filepath=workingloc)
        hmacpath = self.location+".hmac"
        self.save(value=hmacval, filepath=hmacpath)
        tools.rename(workingloc, self.location)

    def save (self, value=None, filepath=None):
        if value is None:
            return False
        if filepath is None:
            return False

        tlocalfile = tmpname.get(filepath, suff=str(os.getpid()))

        f = open(tlocalfile[1], "w")
        f.write(value)
        f.close()

        tools.rename(tlocalfile[1], tlocalfile[0])

    def gethmac (self):
        hmacpath = self.location+".hmac"
        if not os.path.exists(hmacpath):
            return False

        f = open(hmacpath, "r")
        val = f.read()
        f.close()
        return val

    def calchmac (self, filepath=None, key="forban"):

        if not os.path.exists(filepath):
            return False
        f = open (filepath,"r")
        auth = hmac.new(key, f.read(), sha1)
        f.close()

        return auth.hexdigest()

    def cache (self, uuid):
        cachepath = os.path.join (self.lootdir, uuid, "cache")
        if not os.path.exists(cachepath):
            os.makedirs(cachepath)
        lloot = loot.loot()
        for url in lloot.getindexurl(uuid):
            hmacannounced = lloot.gethmac(uuid)
            hmaccalculated = self.calchmac(cachepath+"/forban/index")
            # only fetch the index if the HMAC is different
            if not hmacannounced == hmaccalculated:
                fetch.urlget(url, cachepath+"/forban/index")

    def search (self, query, uuid=None):
        queryresult = []
        pmatch = re.compile(query, re.I)
        if uuid is None:
            location = self.location
        else:
            location = self.lootdir + uuid + "/cache/forban/index"

        f = open(location, "r")
        for cacheline in f.readlines():
            if pmatch.search(cacheline):
                if re.search('/\.',cacheline):
                    continue
                if re.search('^\+\.',cacheline):
                    continue
                queryresult.append(cacheline)
        f.close()

        return queryresult

    def getfilesize (self, filename=None, uuid=None):

        if filename is None:
            return False

        # if uuid is None we use the local cache
        if uuid is None:
            location = self.location
        else:
            location = self.lootdir + uuid + "/cache/forban/index"
        f = open(location, "r")
        pmatch = re.compile(re.escape(filename))
        for line in f.readlines():
            if pmatch.search(line):
                v = line.rsplit(",",1)[1].rstrip('\n')
                return int(v)
        return False

    def totalfilesize (self, uuid=None, prettyprint = True):

        if uuid is None:
            return False
        cachepath = os.path.join(self.lootdir, uuid, "cache","forban","index")

        if not os.path.exists(cachepath):
            return False
        totalvalue = 0
        f = open (cachepath, "r")
        for line in f.readlines():
            val = line.rsplit(",",1)[1].rstrip('\n')
            totalvalue = totalvalue + int(val)

        f.close()

        if prettyprint is False:
            return totalvalue
        else:
            return tools.convertbytes(totalvalue)

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
        f1vs = f1v.splitlines()
        f1vs.sort()
        f2vs = f2v.splitlines()
        f2vs.sort()
        mydiff = '\n'.join(list(difflib.unified_diff(f1vs,f2vs, lineterm="")))
        lmodified = []
        for l in mydiff.splitlines():
            if re.search("(^\+)",l) and not re.search("^\+\+",l) and not re.search("forban",l):
                #exclude temporary files or dot files
                if re.search('/\.',l):
                    continue
                if re.search('^\+\.',l):
                    continue
                missingfile = l.rsplit(",",1)[0]
                missingfile = re.sub("^(\+)","",missingfile)
                lmodified.append(missingfile)
        if lmodified:
            return lmodified
        else:
            return None

def test ():
    testindex = manage()
    testindex.build()
    print testindex.gethmac()

    testindex.cache("8d63025e-2f11-4c08-837a-08c44b122150")
    #print testindex.howfar("e2f05993-eba1-4b94-8e56-d2157d1ce552")
    #print testindex.search("^((?!forban).)*$","e2f05993-eba1-4b94-8e56-d2157d1ce552");
    print testindex.getfilesize(filename="forban/index")
    print testindex.getfilesize(filename="forban//index",uuid="8d63025e-2f11-4c08-837a-08c44b122150")
    print testindex.totalfilesize(uuid="d55727ed-5c6a-49a8-9d8d-28b4004aee0c")

if __name__ == "__main__":

    test()
