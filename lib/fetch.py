# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2013 Alexandre Dulaunoy - http://www.foo.be/
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
import socket
import urllib.request, urllib.error, urllib.parse
import shutil

socket.setdefaulttimeout(10)

import tmpname
import tools

def urlheadinfo(url):
    request = urllib.request.Request(url)
    request.add_header('User-Agent','Forban +http://www.foo.be/forban/')
    request.get_method = lambda: "HEAD"

    try:
        httphead = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        return False
    except urllib.error.URLError as e:
        return False
    else:
        pass

    return (httphead.headers["last-modified"],httphead.headers["content-length"])

def urlget(url, localfile="testurlget"):
    httpreq = urllib.request.Request(url)
    httpreq.add_header('User-Agent','Forban +http://www.foo.be/forban/')

    try:
        r = urllib.request.urlopen(httpreq)
    except urllib.error.HTTPError as e:
        return False
    except urllib.error.URLError as e:
        return False
    except socket.error as e:
        return False
    except socket.timeout:
        return False
    else:
        pass

    (lpath, lfile) = os.path.split(localfile)

    if not os.path.isdir(lpath) and not (lpath ==''):
        os.makedirs(lpath)

    # as url fetch is part of the Forban protocol interface
    # the Content-Disposition MUST be present even if it's
    # not used right now. The interface is used as file transfert
    # so the Content-Disposition is a requirement for any other
    # HTTP clients

    tlocalfile = tmpname.get(localfile)

    if 'Content-Disposition' in r.info():
        f = open(tlocalfile[1], "wb")
        try:
            shutil.copyfileobj(r, f)
        except:
            return False
        f.close()
        if os.path.exists(tlocalfile[1]):
            tools.rename(tlocalfile[1], tlocalfile[0])
        return True
    else:
        return False

def managetest():
    print((urlget("http://127.0.0.1:12555/s/?g=forban/index")))

if __name__ == "__main__":
    managetest()

