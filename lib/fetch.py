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
import socket
import urllib2
import shutil

socket.setdefaulttimeout(10)

import tmpname
import tools

def urlheadinfo(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent','Forban +http://www.gitorious.org/forban/')
    request.get_method = lambda: "HEAD"

    try:
        httphead = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        return False
    except urllib2.URLError, e:
        return False
    else:
        pass

    return (httphead.headers["last-modified"],httphead.headers["content-length"])

def urlget(url, localfile="testurlget"):
    httpreq = urllib2.Request(url)
    httpreq.add_header('User-Agent','Forban +http://www.gitorious.org/forban/')

    try:
        r = urllib2.urlopen(httpreq)
    except urllib2.HTTPError, e:
        return False
    except urllib2.URLError, e:
        return False
    except socket.error,e:
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

    if r.info().has_key('Content-Disposition'):
        f = open (tlocalfile[1], "w")
        try:
            shutil.copyfileobj(r.fp,f)
        except:
            return False
        f.close()
        if os.path.exists(tlocalfile[1]):
            tools.rename(tlocalfile[1], tlocalfile[0])
        return True
    else:
        return False

def managetest():
    #urlget("http://192.168.154.199:12555/s/?g=forban/index")
    print urlget("http://192.168.1.4:12555/s/?g=forban/index")

if __name__ == "__main__":
    managetest()

