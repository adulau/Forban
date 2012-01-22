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

import base64

def encode( istring ):
    b64s = base64.urlsafe_b64encode(istring)
    b64s = b64s.replace("=","!")
    return b64s

def decode( istring ):
    istring = istring.replace("!","=")
    b64s = base64.urlsafe_b64decode(istring.encode("utf-8"))
    return b64s

if __name__ == "__main__":
    encodedone = encode("some string with")
    print encodedone
    decodedone = decode(encodedone)
    print decodedone
