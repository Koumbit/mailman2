# -*- python -*-
# $URL$
# $Id$

"""Find languages used by mailing list at a site.

This module is intended to be used in a withlist context.

  withlist -q -a -r used_languages
    show list of languages enabled in any mailing list.

  withlist -q -a -r used_languages.show
    For each mailing list print a line containing the
    URL for its language page and enabled languages.

  withlist -q -a -r used_languages.show_intl
    Same as above omitting mailing lists that have only
    english enabled.

This module must be installed in a directory on withlist's
python path, choose /usr/lib/mailman/pythonlib for now.
"""#

import sys, atexit, cStringIO

all_languages = {}
out = None

def used_languages(mlist):
    global out
    for l in mlist.available_languages:
        all_languages[l] = True
    out = cStringIO.StringIO()
    used = all_languages.keys()
    used.sort()
    print >>out, ' '.join(used)

def show(mlist):
    langs = mlist.available_languages
    print '%s/language: %s' % (mlist.GetScriptURL('admin',1), ', '.join(langs))

def show_intl(mlist):
    langs = mlist.available_languages
    if langs != ['en']:
        print '%s/language: %s' % (mlist.GetScriptURL('admin',1), ', '.join(langs))

def _result():
    if out:
        sys.stdout.write(out.getvalue())

atexit.register(_result)



