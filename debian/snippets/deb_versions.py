#! /usr/bin/python -O
# $URL$
# $Id$


def _int(v):
    try:
        v = int(v)
    except ValueError:
        pass
    return v

class DebianVersion:

    def __init__(self, ver):
        """
        TBD: add epoch support
        """#
        version = ver.split('-')
        if len(version) == 1:
            ups = version[0]
        elif len(version) == 2:
            ups, rev = version
        else:
            raise ValueError(ver)
        self._ups = [ _int(c) for c in ups.split('.') ]
        self._rev = [ _int(c) for c in rev.split('.') ]

    def __cmp__(self, other):
        diff = cmp(self._ups, other._ups)
        if diff == 0:
            diff = cmp(self._rev, other._rev)
        return diff

    def __str__(self):
        ups = '.'.join([ str(i) for i in self._ups])
        rev = '.'.join([ str(i) for i in self._rev])
        return '-'.join((ups, rev))


if __name__ == '__main__':
    DV = DebianVersion

    ancient = DV('2.0.11-1woody8')
    old     = DV('2.1.3-2')
    current = DV('2.1.4.dfsg-4')
    next    = DV('2.1.4-4split0')
    print ancient, old, current, next

    def compare(a,b):
        if a < b: print '%(a)s < %(b)s' % locals()
        elif a > b: print '%(a)s > %(b)s' % locals()
        elif a == b: print '%(a)s == %(b)s' % locals()
        else: print '%(a)s and %(b)s don\'t compare!' % locals()

    compare(ancient, next)
    compare(next, current)
