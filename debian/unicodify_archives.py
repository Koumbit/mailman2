#! @PYTHON@
#
# Copyright (C) 2007 Lionel Elie Mamane <lmamane@debian.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

"""Convert a list's archive databases to unicode where appropriate

This script is intended to be run as a bin/withlist script, i.e.

% bin/withlist -l -r unicodify_archives <mylist>
"""

import paths
import time
from Mailman.i18n import _
from Mailman import mm_cfg

def unicodify_string(s):
    if isinstance(s,unicode):
        return s
    elif isinstance(s,str):
        try:
            return s.decode()
        except UnicodeDecodeError:
            pass
        try:
            return s.decode('utf-8')
        except UnicodeDecodeError:
            pass
        return s.decode('windows-1252', 'replace')

def unicodify_fst(t):
    l = list(t[1:])
    l.insert(0, unicodify_string(t[0]))
    return tuple(l)

def unicodify_archives(mlist):
    # Only act if we are using the internal archiver
    if mm_cfg.PUBLIC_EXTERNAL_ARCHIVER:
        return
    else:
        from Mailman.Archiver import HyperArch
        h = HyperArch.HyperArchive(mlist)
        currentVolume = h.dateToVolName(time.time())
        if currentVolume in h.archives:
            for hdr in ('subject', 'author'):
                h.database.mapKeys(unicodify_fst, currentVolume, hdr)
        h.close()



if __name__ == '__main__':
    print _(__doc__.replace('%', '%%'))
