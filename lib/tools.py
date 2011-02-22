# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2011 Alexandre Dulaunoy - http://www.foo.be/
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
import platform
import re

def convertbytes (bytes=None):

    if bytes is None:
        return False

    bytes = float(bytes)

    if bytes >= 1099511627776:
        tera = bytes / 1099511627776
        cbytes = '%.2fTB' % tera
    elif bytes >= 1073741824:
        giga = bytes / 1073741824
        cbytes = '%.2fGB' % giga
    elif bytes >= 1048576:
        mega = bytes / 1048576
        cbytes = '%.2fMB' % mega
    elif bytes >= 1024:
        kilo = bytes / 1024
        cbytes = '%.2fKB' % kilo
    else:
        cbytes = '%.2fb' % bytes

    return cbytes

# Rename function to handle the platform specific case
# especially with Windows platform.

def rename(source=None, destination=None):

    if source is None or destination is None:
        return False

    if not os.path.exists(source):
        return False

    sys = platform.system()

    if sys == "Windows":
        if os.path.exists(destination):
            os.remove(destination)
        os.rename(source, destination)

    else:
        os.rename(source, destination)

# Guess local hostname on Unix and Windows
#

def guesshostname():
    guessedhostname = platform.node()
    return guessedhostname

# Return a list of tuple (filepath, size, mtime) for a directory
#

def dirtree(rootdir=None):
    if rootdir==None:
        return False
    if not os.path.exists(rootdir):
        return False

    index = []

    for root, dirs, files in os.walk(rootdir, topdown=True):
        for name in files:
            try:
                filename = os.path.join(root, name)
                filenamesize = str(os.path.getsize(os.path.join(root,name)))
                filenamemtime = str(os.path.getmtime(os.path.join(root,name)))
                index.append((filename,filenamesize,filenamemtime))
            except:
                pass

    return index

# Return a list of directories matching a pattern
#

def finddir(rootdir=None, dirmatch="forban"):
    if rootdir==None:
        return False
    if not os.path.exists(rootdir):
        return False

    dirfound = []

    for root, dirs, files in os.walk(rootdir, topdown=True):
        for name in dirs:
            if re.search(name, dirmatch):
                if os.path.isdir(os.path.join(root,name)):
                    dirpath = str(os.path.join(root,name))
                    dirfound.append(dirpath)

    return dirfound

if __name__ == "__main__":
   print convertbytes (1234567)
   print guesshostname()
   print finddir("/media")
   # print rename("x","xy")
