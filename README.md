Forban
======

[Forban](http://www.foo.be/forban/) is a p2p application for link-local and local area network.

Forban works independently from Internet and use only the local 
area capabilities to announce, discover, search or share files. 
Forban relies on HTTP and he is opportunistic.

The name took his origins from the old French word : 
http://fr.wiktionary.org/wiki/forban 

Forban name can be also a playword in English
for banning an unwanted software or services on Internet.

Forban is free software licensed under 
the GNU Affero General Public License version 3.
http://www.fsf.org/licensing/licenses/agpl-3.0.html

Installation
------------

The setup is quite easy :                             

Clone the repository:

    git clone git@github.com:adulau/Forban.git

Go to the cloned directory:

    cd Forban

and starts Forban processes:

    ./bin/forbanctl start

Now you can open your favorite browser at the following location:

    http://127.0.0.1:12555

To share some files, you'll just need to copy them in ./var/share/ 

Forban protocol
--------------- 

### message format used for announce/discovery

### announce message

ASCII encoded message using UDP on port 12555 with
the following format: 

    forban;name;<nameoftheforban>;uuid;<identityoftheforban>;hmac;<hmacvaluecofindex>

The messages are flooded in broadcast (IPv4) and using
ff02::1 (IPv6) at a regular interval.

Based on the source IP and the destination port used,
a HTTP URL is build to get to default forban service.

### HTTP services for Forban

The UDP port 12555 is there for announcing forban services.
The TCP port 12555 is the HTTP server running for forban services.

base URL: [REQUIRED]
    http://<ip>:<destport>/

index URL where Forban stored his index: [REQUIRED]
    http://<ip>:<destport>/s/?g=forban/index

store URL where Forban stored his loot and how to get a file: [REQUIRED]
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
or the python base64.urlsafe_b64encode with an addition to
the equal sign being replaced by an exclamation mark.

### Forban mode available

* Opportunistic mode
* Shared mode

The opportunistic mode and shared used all the REQUIRED components of
the protocol. The only difference is the lack of automatic file fetching
in the shared mode. The shared mode is usally used on fixed node content
where the opportunistic fetching is not desired (e.g. a fixed bookshelf).

The opportunistic mode is working as a simple gossip (or epidemic) protocol
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
* There is no additional Python libraries required

