#! /usr/bin/python -O
# $URL$
# $Id$

"""Moves old templates from the ucf cache to our conffile database.

This is needed when upgrading from a MM release that uses ucf.
"""

import sys, os


sys.path.insert(0, '/var/lib/mailman')

mm_languages="big5 ca cs da de en es et eu fi fr gb hr hu it ja ko lt nl no pl pt pt_BR ro ru sl sr sv uk".split()


def ucf_to_cfdb():
    from Mailman.Debian import cfdb

    UCF_CACHE = '/var/lib/ucf/cache'
    ETC_DIR   = '/etc/mailman/'
    ETC_LEN   = len(ETC_DIR)

    prev_lang = None

    for cached in os.listdir(UCF_CACHE):
        path = '/'.join(cached.split(':'))
        if not path.startswith(ETC_DIR):
            continue
        try:
            reg_key = path[ETC_LEN:]
            lang, tmpl = reg_key.split('/')
            if lang in mm_languages:
                if lang != prev_lang:
                    if prev_lang: db.sync()
                    prev_lang = lang
                    cfdb.register(lang, None)
                tmpl = open(os.path.join(UCF_CACHE, cached)).read()
                cfdb.register(reg_key, tmpl)
        except ValueError:
            tmpl = open(os.path.join(UCF_CACHE, cached)).read()
            cfdb.register(path, tmpl)

        os.system('ucf --purge %(path)s' % locals())

    cfdb.close()

if __name__ == '__main__':
    ucf_to_cfdb()
