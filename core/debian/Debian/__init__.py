# $URL$
# $Id$

from helpers   import *
from cf_db     import ConfFileDatabase

try:
    from templates import mm_cfg_defaults, mm_cfg_fillin, mm_cfg_deprecated, mm_crontab
except ImportError:
    pass

mm_languages="big5 ca cs da de en es et eu fi fr gb hr hu it ja ko lt nl no pl pt pt_BR ro ru sl sr sv tr uk".split()

cfdb = ConfFileDatabase('/var/lib/mailman/data/debcf.db')

__all__ = [ 'SimpleLogger',
            'DebuggingLogger',
            'CommandRunner',
            ]
