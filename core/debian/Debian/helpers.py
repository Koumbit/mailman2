#! /usr/bin/python -O
#
# Adopted from mailman maintainer scripts
#
# Copyright (c) 2004, Bernd S. Brentrup <bsb@debian.org>
#
# Licensed under GPL version 2
#
# Work in progress, STANDARD NO WARRANTY DISCLAIMER
#
# $URL$
# $Id$

"""
"""#

__version__ = '0.1'

__all__ = [
    'SimpleLogger',
    'DebuggingLogger',
    'CommandRunner',
    ]


# We'll use this copy later in CommandRunner
virgin_gbls = globals().copy()
for k in ('__doc__', '__version__', '__all__'):
    del virgin_gbls[k]

import sys, os

class SimpleLogger:
    """
    """#
    levels = [ 'none', 'some', 'most', 'all' ]

    def __init__(self, prefix):
        self._file = sys.stderr
        try:
            level = os.environ['%(prefix)s_LOG' % locals()]
            self._level = int(level)
        except KeyError:
            self._level = 1
        except ValueError:
            try:
                self._level = self.levels.index(level.lower())
            except ValueError:
                self._level = 0

    def set_level(self, lvl):
        self._level = lvl

    def set_file(self, fl):
        self._file = fl

    def __call__(self, msg, **kw):
        nl = kw.get('nl', '\n')
        lvl = kw.get('lvl', 1)
        if lvl <= self._level:
            self._file.write('%(msg)s%(nl)s' % locals())
            self._file.flush()

    def exception(self, lvl=9):
        """Log exception in sys.exc_info."""
        import traceback as tb
        self(''.join(tb.format_exception(*sys.exc_info())),
             lvl=lvl)

class DebuggingLogger(SimpleLogger):
    """
    """#

    def __init__(self, prefix):
        SimpleLogger.__init__(self, prefix)
        self._info = [ 'modules', 'path', 'argv', 'version', 'environ' ]
        try:
            info = os.environ['%(prefix)s_DEBUG' % locals()]
            if info not in ('all', 'chatty'):
                self._info = info.split(',')
            elif info == 'chatty':
                self.set_level(999)
        except:
            self._info = []

    def sys_info(self):
        if 'modules' in self._info:
            for n, m in sys.modules.items():
                if m is not None:
                    self('%20s: %r' % (n, m), lvl=0)
            self('', lvl=0)
        if 'version' in self._info:
            self('sys.version=%r' % sys.version, lvl=0)
            self('', lvl=0)
        if 'path' in self._info:
            self('sys.path=%r' % sys.path, lvl=0)
            self('', lvl=0)
        if 'argv' in self._info:
            self('sys.argv=%r' % sys.argv, lvl=0)
            self('', lvl=0)
        if 'environ' in self._info:
            self('os.environ:', lvl=0)
            for n, v in os.environ.items():
                self('%20s=%r' % (n, v), lvl=0)
            self('', lvl=0)

class CommandRunner:
    """
    """#

    def __init__(self, prepend=None):
        self._prepend = prepend


    def run(self, cmd, *args):
        """
        """#
        gbls = virgin_gbls.copy()
        sys_argv    = sys.argv[:]
        sys_path    = sys.path[:]
        sys.argv    = [cmd] + list(args)
        if self._prepend:
            sys.path.insert(0, self._prepend)
        execfile(cmd, gbls)
        sys.path    = sys_path
        sys.argv    = sys_argv

# If run as a script, provide debug info for MM commands
# implemented in Python.

if __name__ == '__main__':
    MM_ROOT = '/var/lib/mailman'
    sys.stderr = sys.stdout
    log = DebuggingLogger('MM_MAINT')
    try:
        CommandRunner(os.path.join(MM_ROOT, 'bin')
                      ).run(*sys.argv[1:])
    finally:
        # If things break, show useful information
        # depending on $MM_MAINT_DEBUG settings
        log.sys_info()
