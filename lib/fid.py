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

#
# forban UUID

import uuid
import os.path

class manage:

    def __init__ (self, dynpath = "../var/"):

        self.dynpath = dynpath
        self.fidpath = os.path.join(dynpath,"fid")
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

