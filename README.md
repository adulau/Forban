Forban
======

[Forban](http://www.foo.be/forban/) is a p2p application for link-local and local area networks.

Forban works independently from the Internet and uses only the local 
area capabilities to announce, discover, search or share files. 
Forban relies on HTTP and it is "opportunistic".

The name takes its origins from an old French word: 
http://fr.wiktionary.org/wiki/forban 

Forban name can also be a playword in English
for banning unwanted software or services on the Internet.

Forban is free software licensed under 
the GNU Affero General Public License version 3.
http://www.fsf.org/licensing/licenses/agpl-3.0.html

A [Forban presentation](http://www.foo.be/forban/pres/2011-FOSDEM-Forban-Intro.pdf) was given at FOSDEM 2011
and another [Forban presentation](http://www.foo.be/haxogreen2012/forban-general.pdf) was given at HAXOGREEN 2012.

Installation
------------

The setup is quite easy :                             

Clone the repository:

    git clone git@github.com:adulau/Forban.git

Go to the cloned directory:

    cd Forban

and start the Forban processes:

    ./bin/forbanctl start

Now you can open your favorite browser and go to the following location:

    http://127.0.0.1:12555

To share some files, you just need to copy them into ./var/share/ 

If you want to use another share directory don't forget
to copy the ./var/share/forban directory, which contains CSS and images
for the website. It can work without these, but it's more handy for
users browsing directly to your Forban in passive mode.

Forban protocol
--------------- 

### message format used for announce/discovery

### announce message

ASCII encoded message use UDP on port 12555 with
the following format: 

    forban;name;<nameoftheforban>;uuid;<identityoftheforban>;hmac;<hmacvaluecofindex>

The messages are flooded in broadcast (IPv4) and use
ff02::1 (IPv6) at a regular interval.

Based on the source IP and the destination port used,
a HTTP URL is built to get to default forban service.

### HTTP services for Forban

The UDP port 12555 is for announcing forban services.
The TCP port 12555 is the HTTP server running forban services.

base URL: [REQUIRED]
    http://<ip>:<destport>/

index URL where Forban stores its index: [REQUIRED]
    http://<ip>:<destport>/s/?g=forban/index

store URL where Forban stores its files and how to get a file: [REQUIRED]
    http://<ip>:<destport>/s/?g=base64_urlsafe(<filenamefromindex>)&f=b64e

search URL: [OPTIONAL]
    http://<ip>:<destport>/q/?v=<yoursearch>&r=<refreshtimeinsec>

REQUIRED interfaces are required to have a full operational Forban
protocol in all the modes. The OPTIONAL interfaces are not required
for machine-to-machine interaction but used to ease the life of the users.

### base64_urlsafe function (b64e)

'+' is replaced by '-'.
'/' is replaced by '_'(underscore).
'=' is replaced by '!'.

This is following the same approach of MIME::Base64::URLSafe
or the python base64.urlsafe_b64encode with an addition of
the equal sign being replaced by an exclamation mark.

### Forban mode available

* Opportunistic mode
* Shared mode

The opportunistic mode and shared mode use all the REQUIRED components of
the protocol. The only difference is the lack of automatic file fetching
in the shared mode. The shared mode is usually used in a fixed node content
where the opportunistic fetching is not desired (e.g. a fixed bookshelf).

The opportunistic mode works as a simple gossip (or epidemic) protocol
to replicate the information from one local to another local Forban.

### message format - notes about HMAC

The optional HMAC value has two purposes :

* To know if the index has been updated
* and to verify (if a PSK is set) if the index has been tampered.

When a PSK is not set, the default PSK value is 'Forban'.

The value is optional as other Forban can download any index when they
want.

### software required

* Python (tested successfully with 2.5, 2.6 and 2.7) - 2.5 is required for the uuid library
* There are no additional Python libraries required

