import glob
import os.path
import sys
import string
import base64
import ConfigParser
import socket
config = ConfigParser.RawConfigParser()
config.read("../cfg/forban.cfg")

forbanpath = config.get('global','path')
forbandiscoveredloots = forbanpath+"/var/loot/"
forbanname = config.get('global','name')
forbanshareroot = config.get('forban','share')

sys.path.append(forbanpath+"lib/")
import index
import loot

import cherrypy
from cherrypy.lib.static import serve_file
import mimetypes

if socket.has_ipv6:
    bindhost = "::"
else:
    bindhost = "0.0.0.0"

cherrypy.config.update({ 'server.socket_port': 12555 , 'server.socket_host': bindhost, 'tools.static.root':forbanshareroot})

forbanpath = { '/css/style.css': {'tools.staticfile.on': True, 'tools.staticfile.filename':forbanshareroot+'forban/css/x.css'},
               '/img/forban-small.png': {'tools.staticfile.on': True, 'tools.staticfile.filename':forbanshareroot+'forban/img/forban-small.png'}
             }

htmlheader = """<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
lang="en"> <head> <link rel="stylesheet" type="text/css" href="/css/style.css"
/> </head>"""

htmlfooter =  """</div></body></html>"""

htmlnav = """ <body><div id="nav"><a href="/"><img src="/img/forban-small.png" alt="forban
logo : a small island where a binary is going to and coming from" /></a><br /><ul><li><span class="home"><i>%s</i></span></li><li><a
href="http://www.gitorious.org/forban/">Forban (source code)</a></li></ul></div>
""" % forbanname

def mime_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

class Root:
    def index(self, directory=forbanshareroot):
        html = htmlheader
        html += """<br/> <br/> <div class="left inner">
        <h2>Discovered link-local Forban available with their loot in the last 3
        minutes</h2>
        """
        html += htmlnav
        html += "<table>"
        discoveredloot = loot.loot()
        mysourcev4 = discoveredloot.getipv4(discoveredloot.whoami())
        allindex = index.manage()
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
                html += "<td>Missing %s files from this loot" % len(missingfiles)
                html += """ <a href="http://%s:12555/v/%s">[view missing]</a> """ % (mysourcev4,name)
                html += """ <a href="http://%s:12555/l/%s">[view index]</a> """ % (mysourcev4,name)
                if name == discoveredloot.whoami():
                    html += "<td><i>yourself</i></td>"
                html += "</tr>"

        html += "</table>"
        html += htmlfooter
        return html
    
    def q(self, querystring):
        print querystring
        return querystring

    def v(self, uuid):
        mindex = index.manage()
        dloot = loot.loot()
        missingfiles = mindex.howfar(uuid)
        html = htmlheader
        html += """<br/> <br/> <div class="left inner"> <h2>Missing files on your loot from %s </h2>""" % dloot.getname(uuid)
        html += htmlnav
        html += "<table>"
        for filemissed in missingfiles:
            html += "<tr>"
            sourcev4 = dloot.getipv4(uuid)
            sourcev6 = dloot.getipv6(uuid)
            html += """<td>%s</td><td><a
            href="http://%s:12555/s/?g=%s&f=b64">v4</a></td> """ % (filemissed,sourcev4,base64.b64encode(filemissed))
            if sourcev6 is not None:
                html += """<td><a href="http://[%s]:12555/s/?g=%s&f=b64">v6</a></td>""" % (sourcev6, base64.b64encode(filemissed))
            html += "</tr>"

        html += "</table>"
        html += htmlfooter
        return html

    def l(self, uuid):
        mindex = index.manage()
        dloot = loot.loot()
        html = htmlheader

        html += """<br/> <br/> <div class="left inner"> <h2>Files available in loot %s </h2>""" % dloot.getname(uuid)
        html += htmlnav
        html += "<table>"


        for fileinindex in mindex.search("^((?!forban).)*$", uuid):
            filei = fileinindex.rsplit(",",1)[0]
            html += "<tr>"
            sourcev4 = dloot.getipv4(uuid)
            sourcev6 = dloot.getipv6(uuid)
            html += """<td>%s</td><td><a
            href="http://%s:12555/s/?g=%s&f=b64">v4</a></td> """ % (filei,sourcev4,base64.b64encode(filei))
            if sourcev6 is not None:
                html += """<td><a href="http://[%s]:12555/s/?g=%s&f=b64">v6</a></td>""" % (sourcev6, base64.b64encode(filei))
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
            g = base64.b64decode(g)
            print g
        gs = string.replace(g, "..", "")
        gs = forbanshareroot + gs
        mimetypeguessed = mime_type(gs)
        return serve_file(gs, content_type=mimetypeguessed,disposition=True, name=os.path.basename(gs))

    index.exposed = True


if __name__ == '__main__':
    
    root = Root()
    root.s = Download()
    cherrypy.quickstart(root, config=forbanpath)

