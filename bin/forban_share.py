import glob
import os.path
import sys
import string
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read("../cfg/forban.cfg")

forbanpath = config.get('global','path')
forbanname = config.get('global','name')
forbanshareroot = config.get('forban','share')

sys.path.append(forbanpath+"lib/")
import index

import cherrypy
from cherrypy.lib.static import serve_file
import mimetypes

cherrypy.config.update({ 'server.socket_port': 12555 , 'server.socket_host': '::', 'tools.static.root':forbanshareroot})

forbanpath = { '/css/style.css': {'tools.staticfile.on': True, 'tools.staticfile.filename':forbanshareroot+'forban/css/x.css'}}

htmlheader = """<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
lang="en"> <head> <link rel="stylesheet" type="text/css" href="/css/style.css"
/> </head>"""

htmlnav = """ <body><div id="nav"><ul><li><span class="home">Forban <i>%s</i></span></li><li><a
href="http://www.gitorious.org/forban/">Forban (source code)</a></li></ul></div>
""" % forbanname

def mime_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

class Root:
    def index(self, directory=forbanshareroot):
        html = htmlheader
        html += """<div class="left inner">
        <h2>Local Forban available with their loot:</h2>
        <a href="index?directory=%s">Up</a><br />
        """ % os.path.dirname(os.path.abspath(directory))
        html += htmlnav
                
        html += """</div></body></html>"""
        return html
    
    def q(self, querystring):
        print querystring
        return querystring

    index.exposed = True
    q.exposed = True


class Download:
    def index(self, g):
        gs = string.replace(g, "..", "")
        gs = forbanshareroot + gs
        mimetypeguessed = mime_type(gs)
        return serve_file(gs, content_type=mimetypeguessed,disposition=True, name=os.path.basename(gs))

    index.exposed = True


if __name__ == '__main__':
    
    # rebuild forban index
    print "Forban rebuild index"

    forbanindex = index.manage()
    forbanindex.build()

    root = Root()
    root.s = Download()
    cherrypy.quickstart(root, config=forbanpath)

