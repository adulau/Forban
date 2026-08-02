# Forban

[Forban](https://www.foo.be/forban/) is a peer-to-peer (P2P) file-sharing
application designed for link-local and local area networks. It works without
an Internet connection: nodes use the local network to announce themselves,
discover one another, search for files, and share files over HTTP.

Forban is *opportunistic*: in its default mode, a node automatically retrieves
files advertised by other Forban nodes and makes them available to the rest of
the network. This gossip-style replication helps files spread between nearby
nodes without requiring a central server.

The name comes from the old French word
[*forban*](https://fr.wiktionary.org/wiki/forban). It can also be read as the
English phrase "for ban," suggesting software that can keep sharing files even
when Internet services are blocked or unavailable.

Forban is free software licensed under version 3 of the
[GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.html).
Presentations about Forban were given at
[FOSDEM 2011](https://www.foo.be/forban/pres/2011-FOSDEM-Forban-Intro.pdf) and
[HAXOGREEN 2012](https://www.foo.be/haxogreen2012/forban-general.pdf).

## Requirements

- Python 3.10 or newer
- CherryPy 18

Install the Python dependency with:

```console
python3 -m pip install -r requirements.txt
```

## Installation and use

Clone the repository and enter its directory:

```console
git clone https://github.com/adulau/Forban.git
cd Forban
```

Start the Forban services:

```console
./bin/forbanctl start
```

Then open <http://127.0.0.1:12555> in a web browser. To share files, copy them
into `./var/share/`.

Forban works without a configuration file. To customize its mode, shared
directory, network destinations, or other settings, copy the sample
configuration and edit it before starting the services:

```console
cp cfg/forban.cfg-sample cfg/forban.cfg
```

If you configure a different shared directory, copy the `./var/share/forban/`
directory into it as well. That directory contains the CSS and images used by
the web interface. Forban can serve files without these assets, but the browsing
experience will be less polished.

To stop the services, run:

```console
./bin/forbanctl stop
```

## Operating modes

Forban supports two modes. Both modes implement all required parts of the
protocol:

- **Opportunistic mode** (the default) automatically retrieves files discovered
  on other nodes. It behaves like a gossip, or epidemic, protocol and replicates
  files from one local Forban node to another.
- **Shared mode** advertises local files but does not automatically retrieve
  files from other nodes. It is useful for a node that hosts a fixed collection,
  such as a curated digital bookshelf.

Select a mode with the `mode` setting in `cfg/forban.cfg`.

## Forban protocol

### Announcements and discovery

Each node periodically broadcasts an ASCII-encoded announcement over UDP port
12555. IPv4 uses broadcast traffic, while IPv6 uses the `ff02::1` all-nodes
multicast address. An announcement has the following format:

```text
forban;name;<nameoftheforban>;uuid;<identityoftheforban>;hmac;<hmacvalueofindex>
```

The receiving node combines the announcement's source IP address with the
service port to construct the URL of the sender's HTTP service.

### HTTP services

Forban uses UDP port 12555 for announcements and TCP port 12555 for its HTTP
service. The protocol defines the following endpoints:

| Endpoint | Requirement | URL |
| --- | --- | --- |
| Base service | Required | `http://<ip>:<port>/` |
| File index | Required | `http://<ip>:<port>/s/?g=forban/index` |
| Stored file | Required | `http://<ip>:<port>/s/?g=base64_urlsafe(<filename-from-index>)&f=b64e` |
| Search | Optional | `http://<ip>:<port>/q/?v=<search-term>&r=<refresh-time-in-seconds>` |

A node must implement all required endpoints to be fully compatible with the
Forban protocol in either operating mode. The optional search endpoint is
intended for people using the web interface and is not needed for communication
between nodes.

### URL-safe Base64 encoding (`b64e`)

Forban encodes file names using an adapted URL-safe Base64 scheme:

- `+` is replaced with `-`.
- `/` is replaced with `_` (underscore).
- `=` is replaced with `!` (exclamation mark).

This scheme follows the approach used by `MIME::Base64::URLSafe` and Python's
`base64.urlsafe_b64encode`, with the additional replacement of padding (`=`)
with an exclamation mark.

### HMAC field

The optional HMAC value in an announcement serves two purposes:

1. It lets another node determine whether the advertised index has changed.
2. When a pre-shared key (PSK) is configured, it lets the node check whether the
   index was modified in transit.

If no PSK is configured, Forban uses `Forban` as the default value. The HMAC
field is optional because a node can retrieve an index whenever needed instead
of relying on the announcement value to detect changes.
