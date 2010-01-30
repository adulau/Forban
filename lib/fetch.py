import os
import urllib2
import shutil

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
    else:
        pass

    (lpath, lfile) = os.path.split(localfile);
    
    if not os.path.isdir(lpath) and not (lpath ==''):
        os.makedirs(lpath)

    # as url fetch is part of the Forban protocol interface
    # the Content-Disposition MUST be present even if it's
    # not used right now. The interface is used as file transfert
    # so the Content-Disposition is a requirement for any other
    # HTTP clients
    
    if r.info().has_key('Content-Disposition'):
        f = open (localfile, "w")
        shutil.copyfileobj(r.fp,f)
        f.close()
        return True
    else:
        return False

def managetest():
    #urlget("http://192.168.154.199:12555/s/?g=forban/index")
    print urlheadinfo("http://192.168.154.199:12555/s/?g=forban/index")
    
if __name__ == "__main__":
    managetest()

