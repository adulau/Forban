===============
Forban Protocol
===============

.. Use headers in this order #=~-_

:toc: yes
:symrefs: yes
:sortrefs: yes
:compact: yes
:subcompact: no 
:rfcedstyle: no
:comments: no
:inline: yes 
:private: yes   

:author: Alexandre Dulaunoy 
:organization: quuxlabs 
:contact: a@foo.be


:Abstract:
    Forban protocol is a simple Peer-to-Peer (p2p) protocol for local area
    network to exchange files. This memo describes the protocol to announce
    and discover Peer-to-Peer Forban nodes. As Forban is a Web-based protocol,
    this memo includes the convention to reach discovered Forban nodes.

:date: 2010 May 


Introduction
############

Forban protocol allows users and machines on the same local area network to
share and distribute files. The purpose of the protocol is providing a
simple method to share files without a complex setup on intermittent 
local area network.

The Forban protocol is described in two basic operations:

* Discovering Forban nodes
* Accessing the discovered Forban nodes 

The Forban protocol used to announce the Forban nodes is 
a simple flooding protocol using UDP messages.

The Forban nodes serve a Web-based protocol relying on the URL
syntax convention described in this memo. 
  
Applicability Statement
#######################

Forban protocol is intended to function within a local area network where
the number of network nodes is limited (below a thousand of network
nodes).

The protocol is intended to work on intermittent and mobile network
connectivity using IPv4 or IPv6. 

Forban Node Definition
######################

A Forban node is uniquely defined by an UUID as described in [RFC4122]_. 
The UUID MUST be persistent on the Forban node and created 
at the first startup of the Forban node. A Forban node MUST be autonomous
from any other network services beside the access medium and the IPv4/IPv6
network used.

A Forban node SHOULD have a comprehensive name to describe the node. 

A Forban node MAY be connected to more than one network at same time
using different access medium.

Discovery Process
#################

Announce Message
================

An announce message uses the user datagram protocol (UDP) to flood
regularly the network. The message size is limited by the maximum
supported UDP size in IPv4 of 65535 octets minus UDP and IP header. 

The destination UDP port used by default for Forban is port 12555.

The announce messages are text-based messages. The message is composed
of a single line without CR or CRLF at the end. The message always
starts with a beacon named 'forban;' to detect a Forban message. After
the beacon, there is a key-value list separated by ';'.

::

 key = 'name' | 'uuid' | 'hmac'
 value = *OCTET
 forbanmessage = 'forban;'*(key';'value';')

A sample Forban announce message without UDP headers :

::

 forban;name;a sample forban;uuid;d55727ed-5c6a-49a8-9d8d-28b4004aee0c;hmac;9bc2974df7325cd0ecf517c572fe20859aa2c228

Access Process
##############

Forban web-based service MUST use the same port number allocated by
the Forban UDP announce message. As the URL is built based
on the destination port used in the announce, the TCP web-based services 
MUST share the same port.   

Base URL
========

In Forban, the URL to access a Forban is composed by using the announce
message. The URL format is the following constructed with the source
IP of the Forban announce message and the destination port used.

::

 http://[source]:[port]/

Index URL
=========

The index URL is used to fetch the index of the Forban and MUST be present.
The index URL is a composed of the base URL plus a specific path :

::

 http://[baseurl]/s/?g=forban/index

Fetch URL
=========

The fetch URL is used to fetch a specific file from a Forban and
MUST be present. The
fetch URL is composed of the base URL plus a specific path including
the filename of the file name in Base64 ursafe :

::

 http://[baseurl]/s/?g=base64_urlsafe(<filenamefromindex>)&f=b64e




Notation Conventions
####################
The capitalized key words "MUST", "MUST NOT",
"REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and
"OPTIONAL" in this document are to be
interpreted as described in [RFC2119]_.

Terminology
###########

* Forban node - is local area network device supporting the Forban protocol as described in this memo

* Forban index - is the index of files proposed by a Forban node

Editorial Notes
###############
To provide feedback on this draft join the Forban 
mailing list at
`http://groups.google.com/group/forban <http://groups.google.com/group/forban>`_


References
##########

.. [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.
.. [RFC4122] Leach, P., Mealling, M., and R. Salz, "A Universally Unique IDentifier (UUID) URN Namespace", RFC 4122, July 2005.
