#! /usr/bin/env python
# $URL$
# $Id$

import sys
sys.path[0] = '/var/lib/mailman/Mailman'

def_gbls = globals().copy()
usr_mod  = {}
usr_def  = {}
execfile('/var/lib/mailman/Mailman/Defaults.py', def_gbls)
usr_gbls = def_gbls.copy()
execfile('/etc/mailman/mm_cfg.py', usr_gbls)


def same_func(f, g):
    f_code, g_code = f.func_code, g.func_code
    return (f_code.co_filename == g_code.co_filename
            and
            f_code.co_firstlineno == g_code.co_firstlineno)


for var, usr_value in usr_gbls.items():
    try:
        def_value = def_gbls[var]
        if usr_value != def_value:
            usr_mod[var] = 1
    except KeyError:
        # Handle user defined variable here
        usr_def[var] = 1
# Generate commented /etc/mailman/mm_cfg.py.dpkg-dist

for var in usr_mod.keys():
    val = usr_gbls[var]
    if var.startswith('__') or callable(val) and same_func(val, def_gbls[var]):
        del usr_mod[var]

print "User modified variables:"
for var in usr_mod.keys():
    print '  %s:\t%r was %r' % (var, usr_gbls[var], def_gbls[var])

print "User defined variables:"
for var in usr_def.keys():
    print '  %s: \t%r' % (var, usr_gbls[var])
