# -*- python -*-
#
# $URL$
# $Id$
#
# Conffile like treatment for mailman templates.
#
# (c) 2004 winnegan consulting brentrup
#

import os
import bsddb

class ConfFileDatabase:
    """
    Registered templates are stored as strings indexed by their
    paths relative to the templates directory.   
    """#

    def __init__(self, path):
        self.db = bsddb.btopen(path, 'c')

    def register(self, path, template):
        """
        """#
        self.db[path] = template

    replace = register

    def verify(self, key, have, dist):
        try:
            stored = self.db[key]
            return (stored == have, stored == dist)
        except bsddb.error:
            raise KeyError(key)


    def remove_unmod(self, prefix, dst=None, callback=None):
        """Bulk-remove unmodified entries from the system.

        
        """#
        abs_p = os.path.isabs(prefix)
        entries = [ k for k in self.db.keys()
                    if k.startswith(prefix) ]
        not_purged = []
        for k in entries:
            path = abs_p and k or os.path.join(dst, k)
            try:
                cf_data = open(path).read()
                if cf_data == self.db[k]:
                    if callback:
                        callback(path, True)
                    os.remove(path)
                else:
                    if callback:
                        callback(path, False)
                    not_purged.append(path)
                    for ext in ('.dpkg-dist', '.dpkg-new', '.dpkg-old'):
                        if os.path.exists(path+ext):
                            os.remove(path+ext)
                del self.db[k]
            except IOError:
                pass
        return not_purged
            

    def update(self, key, src=None, dst=None, data=None):
        """Update an entry identified by key.

        When new configuration data match the recorded version, no
        action is required.
        Otherwise if the file version matches the recorded version,
        update both the file and the recorded version.
        Otherwise all three versions differ, let the user decide on
        the file version while the recorded version is updated to
        match new data.

        New configuration data may either be given as a string in the
        data keyword argument or as a path via the src argument.

        If key is an absolute path, the dst argument is ignored and
        configuration data must either be passed as a string in the
        data keyword argument or src must be the absolute path of a
        file containing new configuration data.
        """#
        
        # TBD: cope with the case where a conffile exists but there is
        #      no record in the database.  This situation may arise
        #      when modified conffiles have been kept for a disabled
        #      language and that language is reenabled.

        abs_p = os.path.isabs(key)
        dst_path = abs_p and key or os.path.join(dst, key)
        if data is None:
            src_path = abs_p and src or os.path.join(src, key)
            data = open(src_path).read()

        if not os.path.exists(dst_path):
            self.db[key] = data
            fl = open(dst_path, 'w')
            fl.write(data)
            fl.close()
            return 'Configuration file %(dst_path)s created.' % locals()

        cf_recorded = self.db[key]
        if data == cf_recorded:
            return 'Configuration file %(dst_path)s unmodified.' % locals()

        if cf_recorded == open(dst_path).read():
            self.db[key] = data
            fl = open(dst_path, 'w')
            fl.write(data)
            fl.close()
            return 'Configuration file %(dst_path)s updated.' % locals()

        self.db[key] = data
        fl = open(dst_path+'.dpkg-old', 'w')
        fl.write(cf_recorded)
        fl.close()
        fl = open(dst_path+'.dpkg-new', 'w')
        fl.write(data)
        fl.close()
        self.db[key] = data
        return 'Configuration file %(dst_path)s changed.' % locals()


    def keys(self, prefix=None):
        if prefix is None:
            return self.db.keys()
        return [ k for k in self.db.keys() if k.startswith(prefix) ]
            
    
    def __getattr__(self, name):
        if name == 'first':
            return self.db.first
        elif name == 'last':
            return self.db.last
        elif name == 'next':
            return self.db.next
        elif name == 'previous':
            return self.db.previous
        elif name == 'keys':
            return self.db.keys
        elif name == 'set_location':
            return self.db.set_location
        elif name == 'sync':
            return self.db.sync
        elif name == 'close':
            return self.db.close
        elif name == 'has_key':
            return self.db.has_key
        elif name == '__getitem__':
            return self.db.__getitem__
        elif name == '__setitem__':
            return self.db.__setitem__
        elif name == '__delitem__':
            return self.db.__delitem__
        else:
            raise AttributeError(name)
