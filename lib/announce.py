import socket
import string
import time
import datetime
import hashlib, hmac
import re

class message:

    def __init__(self,name=None, uuid=None, port="12555", timestamp=None,
    auth=None):

            self.name       = name
            self.uuid       = uuid
            self.port       = port
            self.payload    = "forban;name;" + self.name + ";"
            self.count      = 0

