#!/bin/bash

python2.5  Makespec.py -p ../../project/forban/lib --onefile -F ../../project/forban/bin/forban_announce.py
python2.5  Build.py ./forban_announce/forban_announce.spec
python2.5  Makespec.py -p ../../project/forban/lib --onefile -F ../../project/forban/bin/forban_discover.py
python2.5  Build.py ./forban_discover/forban_discover.spec
#a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(HOMEPATH,'support/useUnicode.py'), '../../project/forban/bin/forban_share.py', '../../project/forban/lib/ext/cherrypy/__init__.py', '../../project/forban/lib/ext/cherrypy/_cpcgifs.py', '../../project/forban/lib/ext/cherrypy/lib/http.py', '../../project/forban /lib/ext/cherrypy/lib/sessions.py', '../../project/forban/lib/ext/cherrypy/_cprequest.py', '../../project/forban/lib/ext/cherrypy/wsgiserver/__init__.py'], pathex=['../../project/forban/lib', '../../project/forban/lib/ext', '../../project/forban/lib', '../../project/forban/lib/ext/cherrypy', '../../project/fo rban/lib/ext/cherrypy/lib', '../../project/forban/lib/ext/cherrypy/wsgiserver/', '/home/adulau/down/pyinstaller-1.4'])

python2.5  Makespec.py --paths=../../project/forban/lib:../../project/forban/lib/ext/cherrypy:../../project/forban/lib/ext -p ../../project/forban/lib -p ../../project/forban/lib/ext/cherrypy -p ../../project/forban/lib/ext --onefile -F ../../project/forban/bin/forban_share.py
python2.5  Build.py ./forban_share/forban_share.spec
python2.5  Makespec.py -p ../../project/forban/lib --onefile -F ../../project/forban/bin/forban_opportunistic.py
python2.5  Build.py ./forban_opportunistic/forban_opportunistic.spec
mkdir forban
cd forban
mkdir cfg
mkdir bin
cd ..
cp ../../project/forban/cfg/forban.cfg ./forban/cfg/
cp ./forban_announce/dist/forban_announce ./forban/bin
cp ./forban_discover/dist/forban_discover ./forban/bin
cp ./forban_share/dist/forban_share ./forban/bin
cp ./forban_opportunistic/dist/forban_opportunistic ./forban/bin
