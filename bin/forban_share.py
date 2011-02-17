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

import glob
import os.path
import sys
import string
import ConfigParser
import socket
import re

def guesspath():
    pp = os.path.realpath(sys.argv[0])
    lpath = os.path.split(pp)
    bis = os.path.split(lpath[0])
    return bis[0]

config = ConfigParser.RawConfigParser()
config.read(os.path.join(guesspath(),"cfg","forban.cfg"))

try:
    forbanpath = config.get('global','path')
except ConfigParser.Error:
    forbanpath = os.path.join(guesspath())

forbandiscoveredloots = os.path.join(forbanpath,"var","loot")

try:
    forbanmode = config.get('global','mode')
except ConfigParser.Error:
    forbanmode = "opportunistic"

try:
    forbanshareroot = config.get('forban','share')
except ConfigParser.Error:
    forbanshareroot = os.path.join(forbanpath,"var","share/")

forbanpathlib = os.path.join (forbanpath,"lib")
sys.path.append(forbanpathlib)

import index
import loot
import base64e
import tools

try:
    forbanname = config.get('global','name')
except ConfigParser.Error:
    forbanname = tools.guesshostname()

try:
    import cherrypy
    from cherrypy.lib.static import serve_file
except ImportError:
    libexternal = os.path.join(forbanpath,"lib","ext")
    sys.path.append(libexternal)
    import cherrypy
    from cherrypy.lib.static import serve_file

import mimetypes

forbanpathlog=os.path.join(forbanpath,"var","log")
if not os.path.exists(forbanpathlog):
    os.mkdir(forbanpathlog)

forbanpathlogfile=os.path.join(forbanpathlog,"forban_share_access.log")
forbanpathlogfilee=os.path.join(forbanpathlog,"forban_share_error.log")

if socket.has_ipv6:
    try:
        socktest = socket.socket(socket.AF_INET6)
        bindhost = "::"
        socktest.close()
    except:
        bindhost = "0.0.0.0"
else:
    bindhost = "0.0.0.0"

cherrypy.config.update({ 'log.screen': False, 'server.socket_port': 12555 , 'server.socket_host': bindhost, 'tools.static.root':forbanshareroot, 'log.access_file':forbanpathlogfile, 'log.error_file':forbanpathlogfilee, 'request.show_tracebacks': False})

forbanpathcherry = { '/css/style.css': {'tools.staticfile.on': True, 'tools.staticfile.filename':forbanshareroot+'forban/css/x.css'},
               '/img/forban-small.png': {'tools.staticfile.on': True, 'tools.staticfile.filename':forbanshareroot+'forban/img/forban-small.png'}
             }

htmlheader = """<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
lang="en"> <head> <link rel="stylesheet" type="text/css" href="/css/style.css"
/> </head>"""

htmlfooter =  """<div id="w3c"><p><small>Forban is free software released under
the <a href="http://www.gnu.org/licenses/agpl.html">AGPL</a>. For more information about Forban and source code : <a
href="http://www.foo.be/forban/">foo.be/forban/</a>.</small></p></div></div><!--
end wrapper --></div></body></html>"""

htmlnav = """ <body><div id="nav"><a href="/"><img src="/img/forban-small.png" alt="forban
logo : a small island where a stream of bits is going to and coming from"
/></a><br /><ul><li><span class="home">Description : <i>%s</i><br/>Mode : <i>%s</i></span></li>
</ul></div><div id="wrapper">
""" % (forbanname, forbanmode)

def mime_type(filename):
    if re.search('/forban/index',filename):
        return 'text/plain'
    else:
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def forban_geturl(uuid=None, filename=None, protocol="v4"):

    if uuid is None or filename is None:
        return False

    discoveredloot = loot.loot(dynpath=os.path.join(forbanpath,"var"))

    if not discoveredloot.exist(uuid):
        return False

    if protocol == "v4":
        ip = discoveredloot.getipv4(uuid)
    else:
        ip = discoveredloot.getipv6(uuid)

    if protocol == "v4":
        url = "http://%s:12555/s/?g=%s&f=b64e" % (ip,base64e.encode(filename))
    else:
        url = "http://[%s]:12555/s/?g=%s&f=b64e" % (ip,base64e.encode(filename))

    return url

class Root:
    def index(self, directory=forbanshareroot):
        html = htmlheader
        html += htmlnav
        html += """<br/> <br/> <br/> <div class="right inner">"""
        html += """ <h2>Search the loot...</h2> """
        html += """ <form method=get action="q/"><input type="text" name="v" value=""> <input
        type="submit" value="search"></form> """
        html += """</div> <div class="left inner">"""
        html += """ <h2>Discovered link-local Forban available with their loot in the last 3 minutes</h2> """
        html += "<table>"
        html += "<th><td>Access</td><td>Name</td><td>Last seen</td><td>Size</td><td>How many files are missing from yourself?</td><td></td></th>"
        discoveredloot = loot.loot(dynpath=os.path.join(forbanpath,"var"))
        mysourcev4 = discoveredloot.getipv4(discoveredloot.whoami())
        allindex =  index.manage(sharedir=forbanshareroot, forbanglobal=forbanpath)
        for name in discoveredloot.listall():
            if (discoveredloot.exist(name) and discoveredloot.lastannounced(name)):
                allindex.cache(name)
            if discoveredloot.lastannounced(name):
                html += "<tr>"
                rname = discoveredloot.getname(name)
                sourcev4 = discoveredloot.getipv4(name)
                if sourcev4 is not None:
                    html += """<td><a href="http://%s:12555/">v4</a></td> """ % sourcev4
                else:
                    html += """<td></td>"""
                sourcev6 = discoveredloot.getipv6(name)
            
                if sourcev6 is not None:
                    html += """<td><a href="http://[%s]:12555/">v6</a></td> """ % sourcev6
                else:
                    html += """<td></td>"""

                html += "<td>"+rname+"</td>"

                lastseen = discoveredloot.lastannounced(name)

                if lastseen is not None:
                    html += """<td>%s secs ago</td>""" % lastseen
                else:
                    html += "<td>never seen</td>"
                missingfiles = allindex.howfar(name)

                totalsize = allindex.totalfilesize(name)
                html +="<td>%s</td>" % str(totalsize)

                if type(missingfiles) is bool:
                    html += "<td><b>Missing index</b> from this loot"
                elif missingfiles is not None:
                    html += "<td>Missing %s files from this loot" % len(missingfiles)
                else:
                    html += "<td>Missing no files from this loot"

                if name != discoveredloot.whoami():
                    html += """ <a href="http://%s:12555/v/%s">[missing?]</a> """ % (mysourcev4,name)
                    html += """ <a href="http://%s:12555/l/%s">[browse]</a> """ % (mysourcev4,name)
                if name == discoveredloot.whoami():
                    html += """ <a href="/l/%s">[browse]</a> """ % (name)
                    html += "<td><i>yourself</i></td>"
                else:
                    html += "<td></td>"
                html += "</tr>"

        html += "</table></div>"
        html += htmlfooter
        return html
    
    def q(self, v=None, r=None):
        querystring = v
        mindex = index.manage(sharedir=forbanshareroot, forbanglobal=forbanpath)
        discoveredloot = loot.loot(dynpath=os.path.join(forbanpath,"var"))
        searchresult = []
        for name in discoveredloot.listall():
            if (discoveredloot.exist(name) and discoveredloot.lastannounced(name)):
               fileavailable = mindex.search( uuid=name, query=querystring)
               for filefound in fileavailable:
                   searchresult.append((filefound,name))
        searchresult.sort()
        html = htmlheader
        html += "<title>search results of %s</title>" % (querystring)
        if r is not None:
            html += """<meta http-equiv="refresh" content="%s">""" % (r)
        html += "</head>"
        html += htmlnav
        html += """<br/> <br/> <div class="left inner">"""
        previousfile = None
        html += "<table><tr><th>Filename</th><th>Available on</th></tr>"
        for foundfiles in searchresult:

            if foundfiles[0] == previousfile:
                html += """<a href="%s">%s</a> """ % (forban_geturl(uuid=foundfiles[1],filename=filename),discoveredloot.getname(foundfiles[1]))
            elif previousfile == None:
                filename = foundfiles[0].rsplit(",",1)[0]
                html += """<td>%s</td> <td><a href="%s">%s</a> """ % (foundfiles[0].rsplit(",",1)[0],forban_geturl(uuid=foundfiles[1],filename=filename),discoveredloot.getname(foundfiles[1]))
            else:
                filename = foundfiles[0].rsplit(",",1)[0]
                html += """</td></tr><td>%s</td> <td><a href="%s">%s</a> """ % (foundfiles[0].rsplit(",",1)[0],forban_geturl(uuid=foundfiles[1],filename=filename),discoveredloot.getname(foundfiles[1]))

            previousfile=foundfiles[0]
        html += "</td></tr></table></div>"
        return html

    def v(self, uuid):
        mindex = index.manage(sharedir=forbanshareroot, forbanglobal=forbanpath)
        dloot = loot.loot(dynpath=os.path.join(forbanpath,"var"))
        missingfiles = mindex.howfar(uuid)
        html = htmlheader
        html += """<br/> <br/> <br/> <div class="left inner"> <h2>Missing files on your loot from %s </h2>""" % dloot.getname(uuid)
        html += htmlnav
        html += "<table>"

        if missingfiles is None:

                html += "You are not missing any files with %s " % dloot.getname(uuid)
        else:

            for filemissed in missingfiles:
                html += "<tr>"
                sourcev4 = dloot.getipv4(uuid)
                sourcev6 = dloot.getipv6(uuid)
                html += """<td>%s</td><td><a
                href="http://%s:12555/s/?g=%s&f=b64e">v4</a></td> """ % (filemissed,sourcev4,base64e.encode(filemissed))
                if sourcev6 is not None:
                    html += """<td><a href="http://[%s]:12555/s/?g=%s&f=b64e">v6</a></td>""" % (sourcev6, base64e.encode(filemissed))
                html += "</tr>"

        html += "</table>"
        html += htmlfooter
        return html

    def l(self, uuid):
        mindex = index.manage(sharedir=forbanshareroot, forbanglobal=forbanpath)
        dloot = loot.loot(dynpath=os.path.join(forbanpath,"var"))
        html = htmlheader

        html += """<br/> <br/> <br /> <div class="left inner"> <h2>Files available in loot %s </h2>""" % dloot.getname(uuid)
        html += htmlnav
        html += "<table>"
        html += "<tr><td>Filename</td><td>Fetch</td></tr>"

        for fileinindex in mindex.search("^((?!forban).)*$", uuid):
            filei = fileinindex.rsplit(",",1)[0]
            if re.search('/\.',filei):
                continue
            if re.search('^\+\.',filei):
                continue
            html += "<tr>"
            sourcev4 = dloot.getipv4(uuid)
            sourcev6 = dloot.getipv6(uuid)
            size = tools.convertbytes(mindex.getfilesize(filename=filei,uuid=uuid))
            html += """<td>%s (%s)</td><td><a href="/s/?g=%s&f=b64e">get</a></td> """ % (filei,size,base64e.encode(filei))
            html += "</tr>"

        html += "</table>"
        html += htmlfooter
        return html

    index.exposed = True
    q.exposed = True
    v.exposed = True
    l.exposed = True

class Download:
    def index(self, g=None, f=None):
        if f is not None:
            g = base64e.decode(g)
        gs = string.replace(g, "..", "")
        gs = forbanshareroot + gs
        mimetypeguessed = mime_type(gs)
        return serve_file(gs, content_type=mimetypeguessed,disposition=True, name=os.path.basename(gs))

    index.exposed = True


if __name__ == '__main__':
    
    root = Root()
    root.s = Download()
    cherrypy.quickstart(root, config=forbanpathcherry)

