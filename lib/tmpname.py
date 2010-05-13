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

try:
    from hashlib import sha1
except ImportError:
    from sha import sha as sha1

#
# return a tuple with the original filename and the temporary reverse name
# (should be unique but reversible per filename)
#

def get(filename=None, suff=None):

    if filename is None:
        return False

    (lpath, lfile) = os.path.split(filename)

    if suff is None:
        h = sha1()
        h.update(lfile)
        hv = h.hexdigest()[:8]
        lfile = "."+lfile+"-"+hv
    else :
        lfile = "."+lfile+"-"+str(suff)

    return (filename,os.path.join(lpath,lfile))

if __name__ == "__main__":
    
    print get("aest")[1]
    print get("/a/b/aestb")
