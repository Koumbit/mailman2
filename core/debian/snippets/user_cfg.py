#! /usr/bin/env python
# $URL$
# $Id$

# Use a 2.0 mm_cfg.py
USER_MM_CFG = '/root/stable/etc/mailman/mm_cfg.py'
# Use a 2.1.4 mm_cfg.py
#USER_MM_CFG = '/etc/mailman/mm_cfg.py'

import sys
sys.path.insert(0, '/usr/lib/mailman')

virgin_gbls = globals().copy()


deprecated = {
    'DEFAULT_HOST_NAME' : '''\
# Replaced by DEFAULT_EMAIL_HOST
# DEFAULT_HOST_NAME = %(DEFAULT_HOST_NAME)r
''',
    'DEFAULT_URL' : '''\
# Replaced by DEFAULT_URL_PATTERN.
# DEFAULT_URL = %(DEFAULT_URL)r
''',
    'OLD_IMAGE_LOGOS' : '''\
# Location has changed.
# IMAGE_LOGOS = %(OLD_IMAGE_LOGOS)r
''',
    }
    
    


def upgrade_mm_cfg():
    def_gbls = virgin_gbls.copy()
    exec 'from Mailman.Defaults import *' in def_gbls
    usr_gbls = virgin_gbls.copy()
    sys.modules['Defaults'] = sys.modules['Mailman.Defaults']
    execfile(USER_MM_CFG, usr_gbls)
    usr_mod  = {}
    usr_def  = {}


    for var, usr_value in usr_gbls.items():
        try:
            def_value = def_gbls[var]
            if usr_value != def_value:
                usr_mod[var] = 1
        except KeyError:
            # Handle user defined variable here
            usr_def[var] = 1

    del usr_mod['__doc__']

    print "User modified variables:"
    for var in usr_mod.keys():
        print '  %s:\t%r was %r' % (var, usr_gbls[var], def_gbls[var])

    print "User defined variables:"
    for var in usr_def.keys():
        print '  %s: \t%r' % (var, usr_gbls[var])

    print

    from urlparse import urlsplit, urlunsplit
    def_scheme, def_netloc, def_path = urlsplit(def_gbls['DEFAULT_URL_PATTERN'])[:3]
    if 'DEFAULT_URL' in usr_mod.keys():
        usr_scheme, usr_netloc, usr_path = urlsplit(usr_gbls['DEFAULT_URL'])[:3]
        usr_gbls['DEFAULT_URL_HOST'] = usr_netloc
        usr_mod['DEFAULT_URL_HOST'] = 1
        if usr_scheme != def_scheme or usr_path != def_path:
            usr_gbls['DEFAULT_URL_PATTERN'] = urlunsplit((usr_scheme, def_netloc, usr_path,
                                                          None, None))
            usr_mod['DEFAULT_URL_PATTERN'] = 1
        usr_gbls['default_url_path'] = usr_path
    elif 'DEFAULT_URL_PATTERN' in usr_mod.keys():
        usr_scheme, usr_netloc, usr_path = urlsplit(usr_gbls['DEFAULT_URL_PATTERN'])[:3]
        usr_gbls['default_url_path'] = usr_path
    else:    
        usr_gbls['default_url_path'] = def_path

    if 'DEFAULT_HOST_NAME' in usr_mod.keys():
        exec 'DEFAULT_EMAIL_HOST = DEFAULT_HOST_NAME' in usr_gbls
        usr_mod['DEFAULT_EMAIL_HOST'] = 1
    if 'IMAGE_LOGOS' in usr_mod.keys():
        if usr_gbls['IMAGE_LOGOS'].startswith('/doc/mailman'):
            exec 'OLD_IMAGE_LOGOS = IMAGE_LOGOS' in usr_gbls
            usr_mod['OLD_IMAGE_LOGOS'] = 1
            usr_gbls['IMAGE_LOGOS'] = def_gbls['IMAGE_LOGOS']
    exec 'DEFAULT_SEND_REMINDERS = DEFAULT_SEND_REMINDERS and True or False' in usr_gbls
    exec 'USE_ENVELOPE_SENDER = USE_ENVELOPE_SENDER and True or False' in usr_gbls

    # Generate commented /etc/mailman/mm_cfg.py.dpkg-dist

    from cStringIO import StringIO
    cfl = StringIO()
    from Mailman.Debian import mm_cfg_defaults, mm_cfg_fillin

    cfl.write(mm_cfg_defaults)
    cfl.write(mm_cfg_fillin % usr_gbls)

    print cfl.getvalue()

    dfl = StringIO()
    dfl.write('#%s\n' % ('-'*71))
    dfl.write('# Variables below are deprecated.  Where applicable, their')
    dfl.write(' values are\n# incorporated above.\n')
    deprecated_vars = deprecated.keys()
    deprecated_vars.sort()
    for v in deprecated_vars:
        try:
            usr_mod[v]
            dfl.write(deprecated[v] % usr_gbls)
        except KeyError: pass

    print dfl.getvalue()

if __name__ == '__main__':
    upgrade_mm_cfg()
