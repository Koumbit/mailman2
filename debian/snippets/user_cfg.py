#! /usr/bin/env python
# $URL$
# $Id$

# Use a 2.0 mm_cfg.py
USER_MM_CFG = '/root/stable/etc/mailman/mm_cfg.py'
# Use a current mm_cfg.py
USER_MM_CFG = '/etc/mailman/mm_cfg.py'

import sys
sys.path.insert(0, '/usr/lib/mailman')

if sys.modules.has_key('Mailman.Defaults'):
    reload(sys.modules['Mailman.Defaults'])
else:
    virgin_gbls = globals().copy()

def keep_mutables(d):
    for k, v in d.items():
        try:
            hash(v)
        except TypeError:
            try:
                d[k] = v.copy()
            except AttributeError:
                d[k] = v[:]

def upgrade_mm_cfg():

    def_gbls = {}
    exec 'from Mailman.Defaults import *' in def_gbls
    keep_mutables(def_gbls)
    usr_gbls = {}
    sys.modules['Defaults'] = sys.modules['Mailman.Defaults']
    execfile(USER_MM_CFG, usr_gbls)

    usr_mod  = {}
    usr_def  = {}


    for var, usr_value in usr_gbls.items():
        try:
            if usr_value != def_gbls[var]:
                usr_mod[var] = 1
        except KeyError:
            # Handle user defined variable here
            usr_def[var] = 1

    del usr_def['__doc__']


    if usr_mod.keys():
        log("User modified variables:", lvl=3)
        for var in usr_mod.keys():
            log('  %18s: %r\n%20s: %r'
                % (var, usr_gbls[var], 'default', def_gbls[var]), lvl=3)

    if usr_def.keys():
        log("User defined variables:", lvl=3)
        for var in usr_def.keys():
            log(' %18s: %r' % (var, usr_gbls[var]), lvl=3)


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
            usr_def['OLD_IMAGE_LOGOS'] = 1
            usr_gbls['IMAGE_LOGOS'] = def_gbls['IMAGE_LOGOS']
    if 'PUBLIC_ARCHIVE_URL' in usr_mod.keys():
        exec 'OLD_PUBLIC_ARCHIVE_URL = PUBLIC_ARCHIVE_URL' in usr_gbls
        exec 'PUBLIC_ARCHIVE_URL=%(PUBLIC_ARCHIVE_URL)r' % def_gbls in usr_gbls
        usr_def['OLD_PUBLIC_ARCHIVE_URL'] = 1
    exec 'DEFAULT_SEND_REMINDERS = DEFAULT_SEND_REMINDERS and True or False' in usr_gbls
    exec 'USE_ENVELOPE_SENDER = USE_ENVELOPE_SENDER and True or False' in usr_gbls

    # Generate commented /etc/mailman/mm_cfg.py.dpkg-dist

    from cStringIO import StringIO
    cfl = StringIO()
    from Mailman.Debian import mm_cfg_defaults, mm_cfg_fillin, mm_cfg_deprecated

    cfl.write(mm_cfg_defaults)
    cfl.write(mm_cfg_fillin % usr_gbls)

    for url_host, email_host in usr_gbls['VIRTUAL_HOSTS'].items():
        if (url_host, email_host) not in ((usr_gbls['DEFAULT_URL_HOST'], usr_gbls['DEFAULT_EMAIL_HOST']),
                                          ('localhost', 'localhost')):
            cfl.write('add_virtualhost(%(url_host)r, %(email_host)r)' % locals())

    dfl = StringIO()
    deprecated_vars = mm_cfg_deprecated.keys()
    deprecated_vars.sort()
    usr_mod.update(usr_def)
    for v in deprecated_vars:
        try:
            usr_mod[v]
            dfl.write(mm_cfg_deprecated[v] % usr_gbls)
        except KeyError: pass
    s = dfl.getvalue()
    if s:
            cfl.write(mm_cfg_deprecated[None])
            cfl.write(s)

    print cfl.getvalue()

##     print "Defaults VIRTUAL_HOSTS=%(VIRTUAL_HOSTS)r" % def_gbls
##     print "mm_cfg   VIRTUAL_HOSTS=%(VIRTUAL_HOSTS)r" % usr_gbls

if __name__ == '__main__':
    from Mailman.Debian import DebuggingLogger
    log = DebuggingLogger('MM_MAINT')
    upgrade_mm_cfg()
