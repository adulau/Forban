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

import os
import platform

# Rename function to handle the platform specific case
# especially with Windows platform.

def rename(source=None, destination=None):

    if source is None or destination is None:
        return False

    sys = platform.system()

    if sys == "Windows":
        if os.path.exists(destination):
            os.remove(destination)
        os.rename(source, destination)

    else:
        os.rename(source, destination)

if __name__ == "__main__":
    
    print rename("x","xy")
